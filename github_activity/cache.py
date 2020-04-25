import pandas as pd
from pathlib import Path

DEFAULT_PATH_CACHE = Path("~/data_github_activity").expanduser()


def _cache_data(query_data, path_cache):
    if path_cache is True:
        path_cache = DEFAULT_PATH_CACHE
    path_cache = Path(path_cache)
    if not path_cache.exists():
        print(f"Creating a new cache at {path_cache}")
        path_cache.mkdir()

    for (org, repo), idata in query_data.groupby(["org", "repo"]):
        path_repo_cache = path_cache.joinpath(org, repo)
        path_repo_cache.mkdir(parents=True, exist_ok=True)

        # First pull issues
        def _categorize_item(item):
            if f"{repo}/issues" in item:
                out = "issue"
            else:
                out = "pr"
            return out

        query_data["kind"] = query_data["url"].map(_categorize_item)

        # PRs cache
        data_prs = query_data.query("kind == 'pr'")
        path_pr_cache = path_repo_cache.joinpath("prs.csv")
        if path_pr_cache.exists():
            prs_cache = pd.read_csv(path_pr_cache)
            prs_cache = prs_cache.append(data_prs, sort=False).drop_duplicates(
                subset=["url"]
            )
        else:
            prs_cache = data_prs
        prs_cache.to_csv(path_pr_cache, index=False)

        # Issues cache
        data_issues = query_data.query("kind == 'issue'")
        path_issues_cache = path_repo_cache.joinpath("issues.csv")
        if path_issues_cache.exists():
            issues_cache = pd.read_csv(path_pr_cache)
            issues_cache = issues_cache.append(data_issues, sort=False).drop_duplicates(
                subset=["url"]
            )
        else:
            issues_cache = data_issues
        issues_cache.to_csv(path_issues_cache, index=False)

        # Comments collect
        data_comments = []
        for _, iitems in idata.iterrows():
            for icomment in iitems["comments"]["edges"]:
                this_comment = {}
                this_comment["author"] = icomment["node"]["author"]["login"]
                if not this_comment["author"]:
                    # This happens if the GitHub user has been deleted
                    # ref: https://github.com/jupyterhub/oauthenticator/pull/224#issuecomment-453211986
                    continue
                this_comment["created"] = icomment["node"]["createdAt"]
                this_comment["url"] = icomment["node"]["url"]
                data_comments.append(this_comment)
        data_comments = pd.DataFrame(data_comments).rename(
            columns={"created": "createdAt"}
        )

        # Comments cache
        path_comments_cache = path_repo_cache.joinpath("comments.csv")
        if path_comments_cache.exists():
            comments_cache = pd.read_csv(path_comments_cache)
            comments_cache = comments_cache.append(
                data_comments, sort=False
            ).drop_duplicates(subset=["url"])
        else:
            comments_cache = data_comments
        comments_cache.to_csv(path_comments_cache, index=False)


ALLOWED_KINDS = ["issues", "comments", "prs"]


def load_from_cache(target, kind, path_cache=None):
    # Checks for correctness and existence of cache
    if path_cache is None:
        path_cache = DEFAULT_PATH_CACHE
    if kind not in ALLOWED_KINDS:
        raise ValueError(f"Kind must be one of {ALLOWED_KINDS}, not {kind}")
    path_cache = Path(path_cache)

    # Resolve org / repo
    parts = target.split("/")
    if len(parts) == 1:
        org = parts[0]
        repo = None
    elif len(parts) == 2:
        org, repo = parts
    else:
        raise ValueError(f"Target must be of form org/repo, got: {target}")

    path_cache_org = path_cache.joinpath(org)
    if not path_cache_org.exists():
        raise ValueError(f"Could not find cache for org: {org}")
    if repo is None:
        repos = [
            ii
            for ii in path_cache_org.glob("*")
            if ii.is_dir() and not ii.name.startswith(".")
        ]
    else:
        repos = [path_cache_org.joinpath(repo)]

    # Now loop through the repos and grab data from the cache
    data = []
    for irepo in repos:
        path_cache_repo = path_cache_org.joinpath(irepo)
        if not path_cache_repo.exists():
            raise ValueError(f"Could not find cache for org/repo: {org}/{repo}")
        path_csv = path_cache_repo.joinpath(f"{kind}.csv")
        data.append(pd.read_csv(path_csv))
    data = pd.concat(data)
    return data


def get_cache_stats(path_cache=None):
    if path_cache is None:
        path_cache = DEFAULT_PATH_CACHE

    out_data = []
    for org in path_cache.glob("*"):
        for repo in org.glob("*"):
            for ipath in repo.glob("*"):
                kind = ipath.with_suffix("").name
                idata = pd.read_csv(ipath)
                mindate = idata["createdAt"].min()
                maxdate = idata["createdAt"].max()
                nrecords = idata.shape[0]
                out_data.append(
                    {
                        "org": org.name,
                        "repo": repo.name,
                        "kind": kind,
                        "start": mindate,
                        "end": maxdate,
                        "nrecords": nrecords,
                    }
                )
    return pd.DataFrame(out_data)
