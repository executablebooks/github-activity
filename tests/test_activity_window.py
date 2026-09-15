"""Tests for changelog activity window filtering."""

import datetime

import pandas as pd
import pytest

from github_activity.github_activity import generate_activity_md, get_activity


def _pr_row(number, title, closed_at):
    return {
        "id": f"PR_{number}",
        "title": title,
        "url": f"https://github.com/jupyterhub/action-k3s-helm/pull/{number}",
        "number": number,
        "state": "MERGED",
        "kind": "pr",
        "org": "jupyterhub",
        "repo": "action-k3s-helm",
        "author": "manics",
        "mergedBy": "manics",
        "committers": ["manics"],
        "reviewers": [],
        "comments": {"edges": []},
        "labels": [],
        "closedAt": closed_at,
        "createdAt": "2022-08-20T10:00:00Z",
        "mergeCommit": {"oid": f"sha{number}"},
        "baseRefName": "master",
    }


def _mock_get_activity_dependencies(
    monkeypatch,
    rows,
    since_dt,
    until_dt,
    since_is_git_ref,
):
    datetime_results = iter(
        [
            (since_dt, since_is_git_ref),
            (until_dt, False),
        ]
    )
    monkeypatch.setattr(
        "github_activity.github_activity._get_datetime_and_type",
        lambda *args, **kwargs: next(datetime_results),
    )
    monkeypatch.setattr(
        "github_activity.github_activity._validate_repository_exists",
        lambda *args, **kwargs: None,
    )

    class FakeGitHubGraphQlQuery:
        def __init__(self, *args, **kwargs):
            self.data = pd.DataFrame(rows)
            self.data.attrs["bot_users"] = set()

        request = lambda self: None  # noqa: E731

    monkeypatch.setattr(
        "github_activity.github_activity.GitHubGraphQlQuery",
        FakeGitHubGraphQlQuery,
    )


@pytest.mark.parametrize("api", [get_activity, generate_activity_md])
@pytest.mark.parametrize(
    "since,since_dt,since_is_git_ref,expected",
    [
        ("v3.0.5", "2022-08-21T13:29:31+00:00", True, [74]),
        ("2022-08-21", "2022-08-21T00:00:00+00:00", False, [73, 74]),
    ],
    ids=["git-ref-exclusive", "date-inclusive"],
)
def test_activity_window(monkeypatch, api, since, since_dt, since_is_git_ref, expected):
    """Both APIs exclude a git-ref boundary but include a date boundary (#79)."""
    since_dt = datetime.datetime.fromisoformat(since_dt)
    until_dt = datetime.datetime(2022, 11, 15, 19, 11, 20, tzinfo=datetime.timezone.utc)
    rows = [
        _pr_row(
            number,
            title,
            f"{since_dt + datetime.timedelta(hours=offset):%Y-%m-%dT%H:%M:%SZ}",
        )
        for number, title, offset in [
            (72, "Closed before boundary", -1),
            (73, "Closed at boundary", 0),
            (74, "Closed after boundary", 1),
        ]
    ]
    _mock_get_activity_dependencies(
        monkeypatch, rows, since_dt, until_dt, since_is_git_ref
    )

    result = api(
        target="jupyterhub/action-k3s-helm",
        since=since,
        until="2022-11-15T19:11:20Z",
        auth="test-token",
    )

    if api is get_activity:
        assert result["number"].tolist() == expected
    else:
        for number in [72, 73, 74]:
            assert (f"[#{number}]" in result) == (number in expected)


@pytest.mark.parametrize("api", [get_activity, generate_activity_md])
def test_empty_activity(monkeypatch, api):
    """Empty searches return an empty frame or the intended Markdown error."""
    since_dt = datetime.datetime(2022, 8, 21, tzinfo=datetime.timezone.utc)
    until_dt = datetime.datetime(2022, 8, 22, tzinfo=datetime.timezone.utc)
    _mock_get_activity_dependencies(
        monkeypatch, [], since_dt, until_dt, since_is_git_ref=False
    )
    kwargs = dict(
        target="jupyterhub/action-k3s-helm",
        since="2022-08-21",
        until="2022-08-22",
        auth="test-token",
    )

    if api is get_activity:
        assert api(**kwargs).empty
    else:
        with pytest.raises(ValueError, match="No activity found"):
            api(**kwargs)
