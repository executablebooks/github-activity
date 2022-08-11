"""Use the GraphQL api to grab issues/PRs that match a query."""
import datetime
import os
import re
import shlex
import subprocess
import sys
import urllib
from pathlib import Path
from subprocess import PIPE
from subprocess import run
from tempfile import TemporaryDirectory

import dateutil.parser
import numpy as np
import pandas as pd
import pytz
import requests

from .cache import _cache_data
from .graphql import GitHubGraphQlQuery


# The tags and description to use in creating subsets of PRs
TAGS_METADATA_BASE = {
    "new": {
        "tags": ["feature", "new"],
        "pre": ["NEW", "FEAT", "FEATURE"],
        "description": "New features added",
    },
    "enhancement": {
        "tags": ["enhancement", "enhancements"],
        "pre": ["ENH", "ENHANCEMENT", "IMPROVE", "IMP"],
        "description": "Enhancements made",
    },
    "bug": {
        "tags": ["bug", "bugfix", "bugs"],
        "pre": ["FIX", "BUG"],
        "description": "Bugs fixed",
    },
    "maintenance": {
        "tags": ["maintenance", "maint"],
        "pre": ["MAINT", "MNT"],
        "description": "Maintenance and upkeep improvements",
    },
    "documentation": {
        "tags": ["documentation", "docs", "doc"],
        "pre": ["DOC", "DOCS"],
        "description": "Documentation improvements",
    },
    "api_change": {
        "tags": ["api-change", "apichange"],
        "pre": ["BREAK", "BREAKING", "BRK", "UPGRADE"],
        "description": "API and Breaking Changes",
    },
    "deprecate": {
        "tags": ["deprecation", "deprecate"],
        "pre": ["DEPRECATE", "DEPRECATION", "DEP"],
        "description": "Deprecated features",
    },
}


def get_activity(
    target, since, until=None, repo=None, kind=None, auth=None, cache=None
):
    """Return issues/PRs within a date window.

    Parameters
    ----------
    target : string
        The GitHub organization/repo for which you want to grab recent issues/PRs.
        Can either be *just* and organization (e.g., `jupyter`) or a combination
        organization and repo (e.g., `jupyter/notebook`). If the former, all
        repositories for that org will be used. If the latter, only the specified
        repository will be used.
    since : string | None
        Return issues/PRs with activity since this date or git reference. Can be
        any string that is parsed with dateutil.parser.parse.
    until : string | None
        Return issues/PRs with activity until this date or git reference. Can be
        any string that is parsed with dateutil.parser.parse. If none, today's
        date will be used.
    kind : ["issue", "pr"] | None
        Return only issues or PRs. If None, both will be returned.
    auth : string | None
        An authentication token for GitHub. If None, then the environment
        variable `GITHUB_ACCESS_TOKEN` will be tried. If it does not exist,
        then attempt to infer a token from `gh auth status -t`.
    cache : bool | str | None
        Whether to cache the returned results. If None, no caching is
        performed. If True, the cache is located at
        ~/github_activity_data. It is organized as orgname/reponame folders
        with CSV files inside that contain the latest data. If a string it
        is treated as the path to a cache folder.

    Returns
    -------
    query_data : pandas DataFrame
        A munged collection of data returned from your query. This
        will be a combination of issues and PRs.
    """

    org, repo = _parse_target(target)
    if repo:
        # We have org/repo
        search_query = f"repo:{org}/{repo}"
    else:
        # We have just org
        search_query = f"user:{org}"

    if not auth:
        if "GITHUB_ACCESS_TOKEN" in os.environ:
            # Access token is stored in a local environment variable so just use this
            print("Using GH access token stored in `GITHUB_ACCESS_TOKEN`.")
            auth = os.environ.get("GITHUB_ACCESS_TOKEN")
        else:
            # Attempt to use the gh cli if installed
            try:
                out = run(shlex.split("gh auth status -t"), capture_output=True)
                lines = [ii for ii in out.stderr.decode().split("\n") if "Token:" in ii]
                if lines:
                    print("Using GH access token stored via GH CLI.")
                    auth = lines[0].split(": ")[-1].strip()
            except FileNotFoundError:
                print(
                    (
                        "gh cli not found, so will not use it for auth. To download, "
                        "see https://cli.github.com/"
                    )
                )
        # We can't use this without auth because we hit rate limits immediately
        if not auth:
            raise ValueError(
                "Either the environment variable GITHUB_ACCESS_TOKEN or the "
                "--auth flag or must be used to pass a Personal Access Token "
                "needed by the GitHub API. You can generate a token at "
                "https://github.com/settings/tokens/new. Note that while "
                "working with a public repository, you don’t need to set any "
                "scopes on the token you create. Alternatively, you may log-in "
                "via the GitHub CLI (`gh auth login`)."
            )

    # Figure out dates for our query
    since_dt, since_is_git_ref = _get_datetime_and_type(org, repo, since, auth)
    until_dt, until_is_git_ref = _get_datetime_and_type(org, repo, until, auth)
    since_dt_str = f"{since_dt:%Y-%m-%dT%H:%M:%SZ}"
    until_dt_str = f"{until_dt:%Y-%m-%dT%H:%M:%SZ}"

    if kind:
        allowed_kinds = ["issue", "pr"]
        if kind not in allowed_kinds:
            raise ValueError(f"Kind must be one of {allowed_kinds}")
        search_query += f" type:{kind}"

    # Query for both opened and closed issues/PRs in this window
    print(f"Running search query:\n{search_query}\n\n", file=sys.stderr)
    query_data = []
    for activity_type in ["created", "closed"]:
        ii_search_query = (
            search_query + f" {activity_type}:{since_dt_str}..{until_dt_str}"
        )
        qu = GitHubGraphQlQuery(ii_search_query, auth=auth)
        qu.request()
        query_data.append(qu.data)

    query_data = (
        pd.concat(query_data).drop_duplicates(subset=["id"]).reset_index(drop=True)
    )
    query_data.since_dt = since_dt
    query_data.until_dt = until_dt
    query_data.since_dt_str = since_dt_str
    query_data.until_dt_str = until_dt_str
    query_data.since_is_git_ref = since_is_git_ref
    query_data.until_is_git_ref = until_is_git_ref

    if cache:
        _cache_data(query_data, cache)
    return query_data


def generate_all_activity_md(
    target,
    pattern=r"(v?\d+\.\d+\.\d+)$",
    kind=None,
    auth=None,
    tags=None,
    include_issues=False,
    include_opened=False,
    strip_brackets=False,
    branch=None,
):
    """Generate a full markdown changelog of GitHub activity of a repo based on release tags.

    Parameters
    ----------
    target : string
        The GitHub organization/repo for which you want to grab recent issues/PRs.
        Can either be *just* and organization (e.g., `jupyter`) or a combination
        organization and repo (e.g., `jupyter/notebook`). If the former, all
        repositories for that org will be used. If the latter, only the specified
        repository will be used. Can also be a URL to a GitHub org or repo.
    pattern: str
        The expression used to match a release tag.
    kind : ["issue", "pr"] | None
        Return only issues or PRs. If None, both will be returned.
    auth : string | None
        An authentication token for GitHub. If None, then the environment
        variable `GITHUB_ACCESS_TOKEN` will be tried.
    tags : list of strings | None
        A list of the tags to use in generating subsets of PRs for the markdown report.
        Must be one of:

            ['enhancement', 'bugs', 'maintenance', 'documentation', 'api_change']

        If None, all of the above tags will be used.
    include_issues : bool
        Include Issues in the markdown output. Default is False.
    include_opened : bool
        Include a list of opened items in the markdown output. Default is False.
    strip_brackets : bool
        If True, strip any text between brackets at the beginning of the issue/PR title.
        E.g., [MRG], [DOC], etc.
    branch : string | None
        The branch or reference name to filter pull requests by.

    Returns
    -------
    entry: str
        The markdown changelog entry for all of the release tags in the repo.
    """
    # Get the sha and tag name for each tag in the target repo
    with TemporaryDirectory() as td:

        subprocess.run(
            shlex.split(f"git clone https://github.com/{target} repo"), cwd=td
        )
        repo = os.path.join(td, "repo")
        subprocess.run(shlex.split("git fetch origin --tags"), cwd=repo)

        cmd = 'git log --tags --simplify-by-decoration --pretty="format:%h | %D"'
        data = (
            subprocess.check_output(shlex.split(cmd), cwd=repo)
            .decode("utf-8")
            .splitlines()
        )

    # Clean up the raw data
    pattern = f"tag: {pattern}"

    def filter(datum):
        _, tag = datum
        # Handle the HEAD tag if it exists
        if "," in tag:
            tag = tag.split(", ")[1]
        return re.match(pattern, tag) is not None

    data = [d.split(" | ") for (i, d) in enumerate(data)]
    data = [d for d in data if filter(d)]

    # Generate a changelog entry for each version and sha range
    output = ""

    for i in range(len(data) - 1):
        curr_data = data[i]
        prev_data = data[i + 1]

        since = prev_data[0]
        until = curr_data[0]

        # Handle the HEAD tag if it exists
        if "," in curr_data[1]:
            curr_data[1] = curr_data[1].split(",")[1]

        match = re.search(pattern, curr_data[1])
        tag = match.groups()[0]

        print(f"\n({i + 1}/{len(data)})", since, until, tag, file=sys.stderr)
        md = generate_activity_md(
            target,
            since=since,
            heading_level=2,
            until=until,
            auth=auth,
            kind=kind,
            include_issues=include_issues,
            include_opened=include_opened,
            strip_brackets=strip_brackets,
            branch=branch,
        )

        if not md:
            continue

        # Replace the header line with our version tag
        md = "\n".join(md.splitlines()[1:])

        output += f"""
## {tag}
{md}
"""
    return output


def generate_activity_md(
    target,
    since=None,
    until=None,
    kind=None,
    auth=None,
    tags=None,
    include_issues=False,
    include_opened=False,
    strip_brackets=False,
    heading_level=1,
    branch=None,
):
    """Generate a markdown changelog of GitHub activity within a date window.

    Parameters
    ----------
    target : string
        The GitHub organization/repo for which you want to grab recent issues/PRs.
        Can either be *just* and organization (e.g., `jupyter`) or a combination
        organization and repo (e.g., `jupyter/notebook`). If the former, all
        repositories for that org will be used. If the latter, only the specified
        repository will be used. Can also be a URL to a GitHub org or repo.
    since : string | None
        Return issues/PRs with activity since this date or git reference. Can be
        any string that is parsed with dateutil.parser.parse. If None, the date
        of the latest release will be used.
    until : string | None
        Return issues/PRs with activity until this date or git reference. Can be
        any string that is parsed with dateutil.parser.parse. If none, today's
        date will be used.
    kind : ["issue", "pr"] | None
        Return only issues or PRs. If None, both will be returned.
    auth : string | None
        An authentication token for GitHub. If None, then the environment
        variable `GITHUB_ACCESS_TOKEN` will be tried.
    tags : list of strings | None
        A list of the tags to use in generating subsets of PRs for the markdown report.
        Must be one of:

            ['enhancement', 'bugs', 'maintenance', 'documentation', 'api_change']

        If None, all of the above tags will be used.
    include_issues : bool
        Include Issues in the markdown output. Default is False.
    include_opened : bool
        Include a list of opened items in the markdown output. Default is False.
    strip_brackets : bool
        If True, strip any text between brackets at the beginning of the issue/PR title.
        E.g., [MRG], [DOC], etc.
    heading_level : int
        Base heading level to use.
        By default, top-level heading is h1, sections are h2.
        With heading_level=2 those are increased to h2 and h3, respectively.
    branch : string | None
        The branch or reference name to filter pull requests by.

    Returns
    -------
    entry: str
        The markdown changelog entry.
    """
    org, repo = _parse_target(target)

    # If no since parameter is given, find the name of the latest release
    # using the _local_ git repostory
    # TODO: Check that local repo matches org/repo
    if since is None:
        since = _get_latest_tag()

    # Grab the data according to our query
    data = get_activity(
        target, since=since, until=until, kind=kind, auth=auth, cache=False
    )
    if data.empty:
        return

    # Collect authors of comments on issues/prs that they didn't open for our attribution list
    comment_response_cutoff = 6  # Comments on a single issue
    comment_others_cutoff = 2  # Comments on issues somebody else has authored
    comment_helpers = []
    all_contributors = []
    for _, iitems in data.iterrows():
        item_commentors = []
        for icomment in iitems["comments"]["edges"]:
            comment_author = icomment["node"]["author"]
            if not comment_author:
                # This happens if the GitHub user has been deleted
                # ref: https://github.com/jupyterhub/oauthenticator/pull/224#issuecomment-453211986
                continue

            comment_author = comment_author["login"]

            # Add to list of commentors on items they didn't author
            if comment_author != iitems["author"]:
                comment_helpers.append(comment_author)

            # Add to list of commentors for this item so we can see how many times they commented
            item_commentors.append(comment_author)

        # Count any commentors that had enough comments on the issue to be a contributor
        item_commentors_counts = pd.value_counts(item_commentors)
        item_commentors_counts = item_commentors_counts[
            item_commentors_counts >= comment_response_cutoff
        ].index.tolist()
        for person in item_commentors_counts:
            all_contributors.append(person)

    comment_contributor_counts = pd.value_counts(comment_helpers)
    all_contributors += comment_contributor_counts[
        comment_contributor_counts >= comment_others_cutoff
    ].index.tolist()

    # Clean up the data a bit
    data["labels"] = data["labels"].map(
        lambda a: [edge["node"]["name"] for edge in a["edges"]]
    )
    data["kind"] = data["url"].map(lambda a: "issue" if "issues/" in a else "pr")

    # Filter the PRs by branch (or ref) if given
    if branch is not None:
        index_names = data[
            (data["kind"] == "pr") & (data["baseRefName"] != branch)
        ].index
        data.drop(index_names, inplace=True)
        if data.empty:
            return

    # Separate into closed and opened
    until_dt_str = data.until_dt_str
    since_dt_str = data.since_dt_str
    closed = data.query("closedAt >= @since_dt_str and closedAt <= @until_dt_str")
    opened = data.query("createdAt >= @since_dt_str and createdAt <= @until_dt_str")

    # Separate into PRs and issues
    closed_prs = closed.query("kind == 'pr'")
    closed_issues = closed.query("kind == 'issue'")
    opened_prs = opened.query("kind == 'pr'")
    opened_issues = opened.query("kind == 'issue'")

    # Remove the PRs/Issues that from "opened" if they were also closed
    mask_open_and_close_pr = opened_prs["id"].map(
        lambda iid: iid in closed_prs["id"].values
    )
    mask_open_and_close_issue = opened_issues["id"].map(
        lambda iid: iid in closed_issues["id"].values
    )
    opened_prs = opened_prs.loc[~mask_open_and_close_pr]
    opened_issues = opened_issues.loc[~mask_open_and_close_issue]

    # Now remove the *closed* PRs (not merged) for our output list
    closed_prs = closed_prs.query("state != 'CLOSED'")

    # Add any author of a merged PR to our contributors list
    all_contributors += closed_prs["author"].unique().tolist()

    # Define categories for a few labels
    if tags is None:
        tags = TAGS_METADATA_BASE.keys()
    if not all(tag in TAGS_METADATA_BASE for tag in tags):
        raise ValueError(
            "You provided an unsupported tag. Tags must be "
            f"one or more of {TAGS_METADATA_BASE.keys()}, You provided:\n"
            f"{tags}"
        )
    tags_metadata = {key: val for key, val in TAGS_METADATA_BASE.items() if key in tags}

    # Initialize our tags with empty metadata
    for key, vals in tags_metadata.items():
        vals.update(
            {
                "mask": None,
                "md": [],
                "data": None,
            }
        )

    # Separate out items by their tag types
    for kind, kindmeta in tags_metadata.items():
        # First find the PRs based on tag
        mask = closed_prs["labels"].map(
            lambda a: any(ii == jj for ii in kindmeta["tags"] for jj in a)
        )
        # Now find PRs based on prefix
        mask_pre = closed_prs["title"].map(
            lambda title: any(f"{ipre}:" in title for ipre in kindmeta["pre"])
        )
        mask = mask | mask_pre

        kindmeta["data"] = closed_prs.loc[mask]
        kindmeta["mask"] = mask

    # All remaining PRs w/o a label go here
    all_masks = np.array(
        [~kindinfo["mask"].values for _, kindinfo in tags_metadata.items()]
    )
    mask_others = all_masks.all(0)
    others = closed_prs.loc[mask_others]
    other_description = (
        "Other merged PRs" if len(others) != len(closed_prs) else "Merged PRs"
    )

    # Add some optional kinds of PRs / issues
    tags_metadata.update(
        dict(others={"description": other_description, "md": [], "data": others})
    )
    if include_issues:
        tags_metadata.update(
            dict(
                closed_issues={
                    "description": "Closed issues",
                    "md": [],
                    "data": closed_issues,
                }
            )
        )
        if include_opened:
            tags_metadata.update(
                dict(
                    opened_issues={
                        "description": "Opened issues",
                        "md": [],
                        "data": opened_issues,
                    }
                )
            )
    if include_opened:
        tags_metadata.update(
            dict(opened_prs={"description": "Opened PRs", "md": [], "data": opened_prs})
        )

    # Generate the markdown
    prs = tags_metadata

    extra_head = "#" * (heading_level - 1)

    for kind, items in prs.items():
        n_orgs = len(items["data"]["org"].unique())
        for org, idata in items["data"].groupby("org"):
            if n_orgs > 1:
                items["md"].append(f"{extra_head}## {org}")
                items["md"].append("")

            for irow, irowdata in items["data"].iterrows():
                author = irowdata["author"]
                ititle = irowdata["title"]
                if strip_brackets and ititle.strip().startswith("[") and "]" in ititle:
                    ititle = ititle.split("]", 1)[-1].strip()
                this_md = f"- {ititle} [#{irowdata['number']}]({irowdata['url']}) ([@{author}](https://github.com/{author}))"
                items["md"].append(this_md)

    # Get functional GitHub references: any git reference or master@{YY-mm-dd}
    if closed_prs.size > 0 and not data.since_is_git_ref:
        since = f"master@{{{data.since_dt:%Y-%m-%d}}}"
        closest_date_start = closed_prs.loc[
            abs(
                pd.to_datetime(closed_prs["closedAt"], utc=True)
                - pd.to_datetime(data.since_dt, utc=True)
            ).idxmin()
        ]
        since_ref = closest_date_start["mergeCommit"]["oid"]
    else:
        since_ref = since

    if closed_prs.size > 0 and not data.until_is_git_ref:
        until = f"master@{{{data.until_dt:%Y-%m-%d}}}"
        closest_date_stop = closed_prs.loc[
            abs(
                pd.to_datetime(closed_prs["closedAt"], utc=True)
                - pd.to_datetime(data.until_dt, utc=True)
            ).idxmin()
        ]
        until_ref = closest_date_stop["mergeCommit"]["oid"]
    else:
        until_ref = until
    # SHAs for our dates to build the GitHub diff URL
    changelog_url = f"https://github.com/{org}/{repo}/compare/{since_ref}...{until_ref}"

    # Build the Markdown
    md = [
        f"{extra_head}# {since}...{until}",
        "",
        f"([full changelog]({changelog_url}))",
    ]
    for kind, info in prs.items():
        if len(info["md"]) > 0:
            md += [""]
            md.append(f"{extra_head}## {info['description']}")
            md += [""]
            md += info["md"]

    # Add a list of author contributions
    all_contributors = sorted(set(all_contributors), key=lambda a: str(a).lower())
    all_contributor_links = []
    for iauthor in all_contributors:
        author_url = f"https://github.com/search?q=repo%3A{org}%2F{repo}+involves%3A{iauthor}+updated%3A{data.since_dt:%Y-%m-%d}..{data.until_dt:%Y-%m-%d}&type=Issues"
        all_contributor_links.append(f"[@{iauthor}]({author_url})")
    contributor_md = " | ".join(all_contributor_links)
    gh_contributors_link = f"https://github.com/{org}/{repo}/graphs/contributors?from={data.since_dt:%Y-%m-%d}&to={data.until_dt:%Y-%m-%d}&type=c"
    md += [""]
    md += [f"{extra_head}## Contributors to this release"]
    md += [""]
    md += [f"([GitHub contributors page for this release]({gh_contributors_link}))"]
    md += [""]
    md += [contributor_md]
    md += [""]
    md = "\n".join(md)
    return md


def extract_comments(comments):
    """Extract the comments returned from GraphQL Issues or PullRequests.

    Parameters
    ----------
    comments: pandas Series
        The comments column in the DataFrame returned by `get_activity`.

    Returns
    -------
    comments: pandas DataFrame
        Each comment with metadata for the query given.
    """
    list_of_comments = [ii["edges"] for ii in comments]
    has_comments = any(jj.get("node") for ii in list_of_comments for jj in ii)

    # If we have no comments, just return None
    if not has_comments:
        return None

    comments = [jj.get("node") for ii in list_of_comments for jj in ii]
    comments = pd.DataFrame(comments)
    comments["author"] = comments["author"].map(
        lambda a: a["login"] if a is not None else a
    )

    # Parse some data about the comments
    url_parts = [ii.split("/") for ii in comments["url"].values]
    url_parts = np.array([(ii[3], ii[4], ii[6]) for ii in url_parts])
    orgs, repos, url_parts = url_parts.T

    issue_id = [ii.split("#")[0] for ii in url_parts]
    comment_id = [ii.split("-")[-1] for ii in url_parts]

    # Assign new variables
    comments["org"] = orgs
    comments["repo"] = repos
    comments["issue_id"] = issue_id
    comments["id"] = comment_id
    return comments


def _parse_target(target):
    """
    Returns (org, repo) based on input such as:

    - executablebooks
    - executablebooks/jupyter-book
    - http(s)://github.com/executablebooks
    - http(s)://github.com/executablebooks/jupyter-book(.git)
    - git@github.com:executablebooks/jupyter-book(.git)
    """
    if target.startswith("http"):
        target = target.split("github.com/")[-1]
    elif "@github.com:" in target:
        target = target.split("@github.com:")[-1]
    if target.endswith(".git"):
        target = target.rsplit(".git", 1)[0]
    parts = target.split("/")
    if len(parts) == 2:
        org, repo = parts
    elif len(parts) == 1:
        (org,) = parts
        repo = None
    else:
        raise ValueError(
            f"Invalid target. Target should be of the form org/repo or a GitHub URL. Got {target}"
        )
    return org, repo


def _get_datetime_and_type(org, repo, datetime_or_git_ref, auth):
    """Return a datetime object and bool indicating if it is a git reference or
    not."""

    # Default a blank datetime_or_git_ref to current UTC time, which makes sense
    # to set the until flags default value.
    if datetime_or_git_ref is None:
        dt = datetime.datetime.now().astimezone(pytz.utc)
        return (dt, False)

    try:
        dt = _get_datetime_from_git_ref(org, repo, datetime_or_git_ref, auth)
        return (dt, True)
    except Exception as ref_error:
        try:
            dt = dateutil.parser.parse(datetime_or_git_ref)
            return (dt, False)
        except Exception as datetime_error:
            raise ValueError(
                "{0} not found as a ref or valid date format".format(
                    datetime_or_git_ref
                )
            )


def _get_datetime_from_git_ref(org, repo, ref, auth):
    """Return a datetime from a git reference."""
    headers = {"Authorization": "Bearer %s" % auth}
    url = f"https://api.github.com/repos/{org}/{repo}/commits/{ref}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return dateutil.parser.parse(response.json()["commit"]["committer"]["date"])


def _get_latest_tag():
    """Return the latest tag name for a given repository by querying the local repo."""
    out = run("git describe --tags".split(), stdout=PIPE)
    tag = out.stdout.decode().rsplit("-", 2)[0]
    return tag
