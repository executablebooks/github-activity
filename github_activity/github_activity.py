"""Use the GraphQL api to grab issues/PRs that match a query."""
import datetime
import dateutil
import pytz
import requests
import urllib

from .graphql import GitHubGraphQlQuery
import pandas as pd
import numpy as np


def get_activity(target, since, until=None, repo=None, kind=None, auth=None):
    """Return issues/PRs within a date window.

    Parameters
    ----------
    target : string
        The GitHub organization/repo for which you want to grab recent issues/PRs.
        Can either be *just* and organization (e.g., `jupyter`) or a combination
        organization and repo (e.g., `jupyter/notebook`). If the former, all
        repositories for that org will be used. If the latter, only the specified
        repository will be used.
    since : string
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
        variable `GITHUB_ACCESS_TOKEN` will be tried.

    Returns
    -------
    query_data : pandas DataFrame
        A munged collection of data returned from your query. This
        will be a combination of issues and PRs.
    """

    org, repo = _parse_target(target)

    if repo:
        # We have org/repo
        search_query = f"repo:{target}"
    else:
        # We have just org
        search_query = f"user:{target}"

    since_dt, since_is_git_ref = _get_datetime_and_type(org, repo, since)
    until_dt, until_is_git_ref = _get_datetime_and_type(org, repo, until)
    since_dt_str = f"{since_dt:%Y-%m-%dT%H:%M:%SZ}"
    until_dt_str = f"{until_dt:%Y-%m-%dT%H:%M:%SZ}"
    search_query += f' updated:{since_dt_str}..{until_dt_str}'

    if kind:
        allowed_kinds = ['issue', 'pr']
        if kind not in allowed_kinds:
            raise ValueError(f"Kind must be one of {allowed_kinds}")
        search_query += f" type:{kind}"

    print(f'Running search query:\n{search_query}\n\n')
    qu = GitHubGraphQlQuery(search_query, auth=auth)
    qu.request()
    qu.data.since_dt = since_dt
    qu.data.until_dt = until_dt
    qu.data.since_dt_str = since_dt_str
    qu.data.until_dt_str = until_dt_str
    qu.data.since_is_git_ref = since_is_git_ref
    qu.data.until_is_git_ref = until_is_git_ref
    return qu.data


def generate_activity_md(target, since, until=None, kind=None, auth=None):
    """Generate a markdown changelog of GitHub activity within a date window.

    Parameters
    ----------
    target : string
        The GitHub organization/repo for which you want to grab recent issues/PRs.
        Can either be *just* and organization (e.g., `jupyter`) or a combination
        organization and repo (e.g., `jupyter/notebook`). If the former, all
        repositories for that org will be used. If the latter, only the specified
        repository will be used.
    since : string
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
        variable `GITHUB_ACCESS_TOKEN` will be tried.

    Returns
    -------
    query_data : pandas DataFrame
        A munged collection of data returned from your query. This
        will be a combination of issues and PRs.
    """
    # Grab the data according to our query
    data = get_activity(target, since=since, until=until, kind=kind, auth=auth)
    if data.empty:
        return

    org, repo = _parse_target(target)

    # Clean up the data a bit
    data['labels'] = data['labels'].map(lambda a: [edge['node']['name'] for edge in a['edges']])
    data['kind'] = data['url'].map(lambda a: "issue" if "issues/" in a else "pr")

    # Separate into closed and opened
    until_dt_str = data.until_dt_str
    since_dt_str = data.since_dt_str
    closed = data.query('closedAt >= @since_dt_str and closedAt <= @until_dt_str')
    opened = data.query('createdAt >= @since_dt_str and createdAt <= @until_dt_str')

    # Separate into PRs and issues
    closed_prs = closed.query("kind == 'pr'")
    closed_issues = closed.query("kind == 'issue'")
    opened_prs = opened.query("kind == 'pr'")
    opened_issues = opened.query("kind == 'issue'")

    # Define categories for a few labels
    tags_metadata = {
        "enhancement": {
            'tags': ["enhancement", "feature", "enhancements"],
            'description': "Enhancements made",
            'mask': None,
            'md': [],
            'data': None,
        },
        "bugs": {
            'tags': ["bug", "bugfix", "bugs"],
            'description': "Bugs fixed",
            'mask': None,
            'md': [],
            'data': None,
        },
        "maintenance": {
            'tags': ["maintenance", "maint"],
            'description': "Maintenance and upkeep improvements",
            'mask': None,
            'md': [],
            'data': None,
        },
        "documentation": {
            'tags': ["documentation", "docs", "doc"],
            'description': "Documentation improvements",
            'mask': None,
            'md': [],
            'data': None,
        },
    }

    # Separate out items by their tag types
    for kind, kindmeta in tags_metadata.items():
        mask = closed_prs['labels'].map(lambda a: any(ii in jj for ii in kindmeta['tags'] for jj in a))
        kindmeta['data'] = closed_prs.loc[mask]
        kindmeta['mask'] = mask

    # All remaining PRs w/o a label go here
    all_masks = np.array([~kindinfo['mask'].values for _, kindinfo in tags_metadata.items()])
    mask_others = all_masks.all(0)
    others = closed_prs.loc[mask_others]

    # Create the markdown file
    tags_metadata_update = dict(
        others={'description': "Other closed PRs", "md": [], 'data': others},
        closed_issues={'description': "Closed issues", "md": [], 'data': closed_issues},
        opened_prs={'description': "Opened PRs", "md": [], 'data': opened_prs},
        opened_issues={'description': "Opened issues", "md": [], 'data': opened_issues}
    )
    tags_metadata.update(tags_metadata_update)
    prs = tags_metadata

    for kind, items in prs.items():
        n_orgs = len(items['data']['org'].unique())
        for org, idata in items['data'].groupby('org'):
            if n_orgs > 1:
                items['md'].append(f'## {org}')
                items['md'].append('')

            for irow, irowdata in items['data'].iterrows():
                author = irowdata['author']
                this_md = f"* {irowdata['title']} [#{irowdata['number']}]({irowdata['url']}) ([@{author}](https://github.com/{author}))"
                items['md'].append(this_md)

    # Get functional GitHub references: any git reference or master@{YY-mm-dd}
    since = since if data.since_is_git_ref else f'master@{{{data.since_dt:%Y-%m-%d}}}'
    until = until if data.until_is_git_ref else f'master@{{{data.until_dt:%Y-%m-%d}}}'
    changelog_url = f'https://github.com/{org}/{repo}/compare/{since}...{until}'

    md = [f"# {since}...{until}", f"([full changelog]({changelog_url}))", ""]
    for kind, info in prs.items():
        if len(info['md']) > 0:
            md += [""]
            md.append(f"## {info['description']}")
            md += info['md']
    md = '\n'.join(md)
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
    list_of_comments = [ii['edges'] for ii in comments]
    has_comments = any(jj.get('node') for ii in list_of_comments for jj in ii)

    # If we have no comments, just return None
    if not has_comments:
        return None

    comments = [jj.get('node') for ii in list_of_comments for jj in ii]
    comments = pd.DataFrame(comments)
    comments['author'] = comments['author'].map(lambda a: a['login'] if a is not None else a)

    # Parse some data about the comments
    url_parts = [ii.split('/') for ii in comments['url'].values]
    url_parts = np.array([(ii[3], ii[4], ii[6]) for ii in url_parts])
    orgs, repos, url_parts = url_parts.T

    issue_id = [ii.split('#')[0] for ii in url_parts]
    comment_id = [ii.split('-')[-1] for ii in url_parts]

    # Assign new variables
    comments['org'] = orgs
    comments['repo'] = repos
    comments['issue_id'] = issue_id
    comments['id'] = comment_id
    return comments


def _parse_target(target):
    parts = target.split('/')
    if len(parts) == 2:
        org, repo = parts
    elif len(parts) == 1:
        org = parts
        repo = None
    else:
        raise ValueError(f"Invalid target. Target should be of the form org/repo. Got {target}")
    return org, repo


def _get_datetime_and_type(org, repo, datetime_or_git_ref):
    """Return a datetime object and bool."""

    is_git_ref = False
    if datetime_or_git_ref is None:
        dt = datetime.datetime.now().astimezone(pytz.utc)
    else:
        try:
            dt = dateutil.parser.parse(datetime_or_git_ref)
        except ValueError as e:
            if repo:
                dt = _get_datetime_from_git_ref(org, repo, datetime_or_git_ref)
                is_git_ref = True
            else:
                raise e

    return dt, is_git_ref


def _get_datetime_from_git_ref(org, repo, ref):
    """Return a datetime from a git reference."""

    response = requests.get(f"https://api.github.com/repos/{org}/{repo}/commits/{ref}")
    response.raise_for_status()
    return dateutil.parser.parse(response.json()["commit"]["committer"]["date"])
