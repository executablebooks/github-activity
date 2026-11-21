import re
from datetime import datetime
from types import SimpleNamespace

import pytest

from github_activity import get_activity
from github_activity.graphql import GitHubGraphQlQuery

START = "2020-01-01T00:00:00Z"
END = "2020-01-01T00:00:07Z"


def mock_search(monkeypatch, timestamps, activity):
    """Serve GitHub's reported total, 1,000 accessible results, and real cursors."""
    calls = []
    nodes = [
        {
            "id": str(number),
            "number": number,
            "url": f"https://github.com/org/repo/pull/{number}",
            "createdAt": stamp if activity == "created" else "2019-01-01T00:00:00Z",
            "closedAt": stamp if activity == "closed" else None,
            "author": {"login": "contributor"},
            "mergedBy": None,
            "reviews": None,
            "commits": None,
            "labels": {"edges": []},
            "reactions": {"totalCount": 0},
        }
        for number, stamp in enumerate(timestamps, 1)
    ]

    def post(url, json, auth):
        query = json["query"]
        kind, start, end = re.search(
            r"(created|closed):([^ ]+)\.\.([^\"]+)", query
        ).groups()
        size = int(re.search(r"first: (\d+), query:", query)[1])
        cursor = re.search(r'after: "(\d+)"', query)
        offset = int(cursor[1]) if cursor else 0
        calls.append((kind, start, end, offset))
        field = kind + "At"
        matches = [row for row in nodes if row[field] and start <= row[field] <= end]
        accessible = matches[:1000]
        page = {
            "issueCount": len(matches),
            "nodes": accessible[offset : offset + size],
            "pageInfo": {
                "endCursor": str(offset + size),
                "hasNextPage": offset + size < len(accessible),
            },
        }
        return SimpleNamespace(status_code=200, json=lambda: {"data": {"search": page}})

    monkeypatch.setattr("github_activity.graphql.requests.post", post)
    monkeypatch.setattr(
        "github_activity.github_activity._validate_repository_exists", lambda *a: None
    )
    monkeypatch.setattr(
        "github_activity.github_activity._get_datetime_and_type",
        lambda org, repo, date, auth: (
            datetime.fromisoformat(date.removesuffix("Z")),
            False,
        ),
    )
    return calls


@pytest.mark.parametrize("activity", ["created", "closed"])
def test_complete_large_window(monkeypatch, activity):
    # The two occupied seconds fall into the same half twice before they split.
    next_second = "2020-01-01T00:00:01Z"
    calls = mock_search(monkeypatch, [START] * 500 + [next_second] * 501, activity)
    data = get_activity("org/repo", since=START, until=END, kind="pr", auth="dummy")
    assert sorted(data["number"]) == list(range(1, 1002))
    # Split on the first response; paging through a truncated parent wastes quota.
    assert [c[3] for c in calls if c[:3] == (activity, START, END)] == [0]
    other = "closed" if activity == "created" else "created"
    assert [c for c in calls if c[0] == other] == [(other, START, END, 0)]


def test_exactly_1000_needs_no_split(monkeypatch):
    calls = mock_search(monkeypatch, [START] * 1000, "created")
    result = get_activity("org", since=START, until=START, kind="pr", auth="dummy")
    assert len(result) == 1000
    assert [c[3] for c in calls if c[0] == "created"] == list(range(0, 1000, 50))


def test_single_second_over_limit(monkeypatch):
    mock_search(monkeypatch, [START] * 1001, "created")
    with pytest.raises(ValueError, match="1,000|1000"):
        get_activity("org/repo", since=START, until=START, kind="pr", auth="dummy")


def test_explicit_page_limit(monkeypatch):
    calls = mock_search(monkeypatch, [START] * 1001, "created")
    query = GitHubGraphQlQuery(
        f"repo:org/repo type:pr created:{START}..{END}", auth="dummy"
    )
    query.request(n_pages=2, n_per_page=10)
    assert query.data["number"].tolist() == list(range(1, 21))
    assert [c[3] for c in calls] == [0, 10]
