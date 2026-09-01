"""Tests for changelog activity window filtering."""

import datetime

import pandas as pd

from github_activity.github_activity import generate_activity_md


def _pr_row(number, title, closed_at, labels=None, created_at=None, merge_oid=None):
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
        "labels": labels or [],
        "closedAt": closed_at,
        "createdAt": created_at or "2022-08-20T10:00:00Z",
        "mergeCommit": {"oid": merge_oid or f"sha{number}"},
        "baseRefName": "master",
    }


def _activity_frame(rows, since_dt, until_dt, since_is_git_ref, until_is_git_ref=False):
    data = pd.DataFrame(rows)
    data.since_dt = since_dt
    data.until_dt = until_dt
    data.since_dt_str = f"{since_dt:%Y-%m-%dT%H:%M:%SZ}"
    data.until_dt_str = f"{until_dt:%Y-%m-%dT%H:%M:%SZ}"
    data.since_is_git_ref = since_is_git_ref
    data.until_is_git_ref = until_is_git_ref
    data.attrs["bot_users"] = set()
    return data


def test_git_ref_since_excludes_pr_closed_at_tag(monkeypatch):
    """A PR whose merge commit is the --since tag must not appear in the changelog.

    GitHub compare `tag...HEAD` is exclusive of the tag. Matching that window
    means a PR closed at the tagged commit's timestamp belongs to the previous
    release. Regression for executablebooks/github-activity#79.
    """
    since_dt = datetime.datetime(2022, 8, 21, 13, 29, 31, tzinfo=datetime.timezone.utc)
    until_dt = datetime.datetime(2022, 11, 15, 19, 11, 20, tzinfo=datetime.timezone.utc)
    data = _activity_frame(
        [
            _pr_row(
                72,
                "Earlier same-day PR",
                "2022-08-21T10:00:00Z",
                labels=["bug"],
            ),
            _pr_row(
                73,
                "Calico 3.24.0 (3.23 manifest URL is broken)",
                "2022-08-21T13:29:31Z",
                labels=["bug"],
                merge_oid="d3c165a02b1c75b6e551da97970eecb401269750",
            ),
            _pr_row(
                74,
                "Add RELEASE.md",
                "2022-08-21T15:22:38Z",
            ),
        ],
        since_dt,
        until_dt,
        since_is_git_ref=True,
        until_is_git_ref=True,
    )
    monkeypatch.setattr(
        "github_activity.github_activity.get_activity", lambda *args, **kwargs: data
    )

    md = generate_activity_md(
        target="jupyterhub/action-k3s-helm",
        since="v3.0.5",
        until="v3.0.6",
    )

    assert "[#73]" not in md
    assert "[#72]" not in md
    assert "[#74]" in md


def test_date_since_still_includes_prs_at_window_start(monkeypatch):
    """A calendar-date --since remains inclusive of activity at that instant."""
    since_dt = datetime.datetime(2022, 8, 21, 0, 0, 0, tzinfo=datetime.timezone.utc)
    until_dt = datetime.datetime(2022, 8, 22, 0, 0, 0, tzinfo=datetime.timezone.utc)
    data = _activity_frame(
        [
            _pr_row(73, "Closed at start of since date", "2022-08-21T00:00:00Z"),
            _pr_row(74, "Closed later the same day", "2022-08-21T15:22:38Z"),
        ],
        since_dt,
        until_dt,
        since_is_git_ref=False,
    )
    monkeypatch.setattr(
        "github_activity.github_activity.get_activity", lambda *args, **kwargs: data
    )

    md = generate_activity_md(
        target="jupyterhub/action-k3s-helm",
        since="2022-08-21",
        until="2022-08-22",
    )

    assert "[#73]" in md
    assert "[#74]" in md
