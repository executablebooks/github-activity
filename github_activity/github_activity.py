"""Use the GraphQL api to grab issues/PRs that match a query."""
from .graphql import GitHubGraphQlQuery
import pandas as pd

def get_activity(target, since, before=None, repo=None, kind=None):
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
        Return issues/PRs with activity since this date. Can be any string that is
        parsed with pd.to_datetime.
    before : string | None
        Return issues/PRs with activity before this date. Can be any string that is
        parsed with pd.to_datetime. If none, today's date will be used.
    kind : ["issue", "pr"] | None
        Return only issues or PRs. If None, both will be returned.

    Returns
    -------
    query_data : pandas DataFrame
        A munged collection of data returned from your query. This
        will be a combination of issues and PRs.
    """
    if before is None:
        time = f">={pd.to_datetime(since):%Y-%m-%d}"
    else:
        time = f"{pd.to_datetime(since):%Y-%m-%d}..{pd.to_datetime(before):%Y-%m-%d}"

    query = f'updated:{time}'

    _, repo = _parse_target(target)
    if repo:
        # We have org/repo
        query += f" repo:{target}"
    else:
        # We have just org
        query += f" user:{target}"

    if kind:
        allowed_kinds = ['issue', 'pr']
        if kind not in allowed_kinds:
            raise ValueError(f"Kind must be one of {allowed_kinds}")
        query += f" type:{kind}"

    print(f'Running query:\n{query}\n\n')
    qu = GitHubGraphQlQuery(query)
    qu.request()
    query_data = qu.data
    return query_data


def generate_activity_md(target, since, before=None, kind=None):
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
        Return issues/PRs with activity since this date. Can be any string that is
        parsed with pd.to_datetime.
    before : string | None
        Return issues/PRs with activity before this date. Can be any string that is
        parsed with pd.to_datetime. If none, today's date will be used.
    kind : ["issue", "pr"] | None
        Return only issues or PRs. If None, both will be returned.

    Returns
    -------
    query_data : pandas DataFrame
        A munged collection of data returned from your query. This
        will be a combination of issues and PRs.
    """
    # Parameter parsing
    if before is None:
        before = 'today'

    # Grab the data according to our query
    data = get_activity(target, since=since, before=before, kind=kind)
    org, repo = _parse_target(target)

    # Clean up the data a bit
    data['labels'] = data['labels'].map(lambda a: [edge['node']['name'] for edge in a['edges']])
    data['kind'] = data['url'].map(lambda a: "issue" if "issues/" in a else "pr")

    # Separate into closed and opened
    closed = data.query('closedAt > @since and closedAt < @before')
    opened = data.query('createdAt > @since and createdAt < @before')

    # Separate into PRs and issues
    closed_prs = closed.query("kind == 'pr'")
    closed_issues = closed.query("kind == 'issue'")

    opened_prs = opened.query("kind == 'pr'")
    opened_issues = opened.query("kind == 'issue'")

    # SHAs for our dates to build the GitHub diff URL
    closest_date_start = closed_prs.loc[abs(pd.to_datetime(closed_prs['closedAt'], utc=True) - pd.to_datetime(since, utc=True)).idxmin()]
    closest_date_stop = closed_prs.loc[abs(pd.to_datetime(closed_prs['closedAt'], utc=True) - pd.to_datetime(before, utc=True)).idxmin()]
    closest_start_sha = closest_date_start['mergeCommit']['oid']
    closest_stop_sha = closest_date_stop['mergeCommit']['oid']
    changelog_url = f"https://github.com/{org}/{repo}/compare/{closest_start_sha}...{closest_stop_sha}"

    # Define categories for a few labels
    feature_tags = ["enhancement"]
    mask_features = closed_prs['labels'].map(lambda a: any(ii in jj for ii in feature_tags for jj in a))
    features = closed_prs.loc[mask_features]

    bug_tags = ["bug", "bugfix"]
    mask_bugs = closed_prs['labels'].map(lambda a: any(ii in jj for ii in bug_tags for jj in a))
    bugs = closed_prs.loc[mask_bugs]

    # All remaining PRs w/o a label go here
    others = closed_prs.loc[(~mask_bugs.values) & (~mask_features)]

    # Create the markdown file
    prs = dict(
        features={'title': "Enhancements made", "md": [], 'data': features},
        bugs={'title': "Bugs fixed", "md": [], 'data': bugs},
        others={'title': "Other closed PRs", "md": [], 'data': others},
        closed_issues={'title': "Closed issues", "md": [], 'data': closed_issues},
        opened_prs={'title': "Opened PRs", "md": [], 'data': opened_prs},
        opened_issues={'title': "Opened issues", "md": [], 'data': opened_issues}
    )

    for kind, items in prs.items():
        n_orgs = len(items['data']['org'].unique())
        for org, idata in items['data'].groupby('org'):
            if n_orgs > 1:
                items['md'].append(f'## {org}')
                items['md'].append('')

            for irow, idata in items['data'].iterrows():
                author = idata['author']
                this_md = f"* {idata['title']} [#{idata['number']}]({idata['url']}) ([@{author}](https://github.com/{author}))"
                items['md'].append(this_md)

    md = [f"# {since}...{before}", f"([full changelog]({changelog_url}))", ""]
    for kind, info in prs.items():
        if len(info['md']) > 0:
            md += [""]
            md.append(f"## {info['title']}")
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