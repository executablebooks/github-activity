# User guide

This tool has two main user interfaces:

1. **A python library**: Given a GitHub org, repository, an initial git reference or date, use the [GitHub GraphQL API](https://developer.github.com/v4/) to return a DataFrame of all issue and PR activity for this time period.
2. **A Command Line Interface** to render this activity as markdown, suitable for generating changelogs or community updates.

These sections describe how to control the major functionality of this tool.

## Generate a markdown changelog

```{note}
Before generating a changelog you should [generate and add a GitHub Access Token](use:token).
```

The easiest way to use `github-activity` to generate activity markdown is to use
the command-line interface. It takes the following form:

```bash
github-activity [<org>/<repo>] --since <date or ref> --until <date or ref>
```

The `[<org>/<repo>]` argument is **optional**.
If you do not give it, then `github-activity` will attempt to infer this value by running `git remote -v` and using either `upstream` or `origin` (preferring `upstream` if both are available).

The (optional) arguments in `--since` (or `-s`) and `--until` (or `-u`) can either be
a date, or a ref (such as a commit hash or tag). `github-activity` will pull the activity between the dates corresponding to these values.

```{margin}
There are many other options with the `github-activity` CLI, run `github-activity -h`
for more information
```

Here's an example on the
[jupyter notebook repository](https://github.com/jupyter/notebook), grabbing all
activity since the latest major release and outputting it to a markdown file.

```
github-activity jupyter/notebook -s 6.0.0 -u 6.0.1 -o sample_notebook_activity.md
```

You can find the [resulting markdown here](sample_notebook_activity).

```{tip}
For repositories that use multiple branches, it may be necessary to filter PRs by a branch name.  This can be done using the `--branch` parameter in the CLI.   Other git references can be used as well in place of a branch name.
```

## Choose a date or a tag to filter activity

By default, `github-activity` will pull the activity _after_ the latest GitHub release or git tag. You can choose to manually control the date ranges as well.

To specify a **start date**, use the `-s` (or `--since`) parameter. To specify an **end date**, use the `-u` or `--until` parameter.

Each of these accepts either:

1. A date string. This can be anything that [`dateutil.parser.parse`](https://dateutil.readthedocs.io/en/stable/parser.html) accepts.
2. A git `ref`. For example, a `commit hash` or a `tag`.

If no `-u` parameter is given, then all activity until today will be included.

(prefixes-and-tags)=

## Split PRs by tags and prefixes

Often you wish to split your PRs into multiple categories so that they are easier
to scan and parse. You may also _only_ want to keep some PRs (e.g. features, or API
changes) while excluding others from your changelog.

`github-activity` uses the GitHub tags as well as PR prefixes to automatically
categorize each PR and display it in a section in your markdown. It roughly
follows the [keepachangelog taxonomy of changes](https://keepachangelog.com/en/1.0.0/).

Below is a list of the supported PR types, as well as the tags / title prefixes
that will be used to identify the right category.

```{include} _build/dirhtml/tags_list.txt

```

```{tip}
You can choose to *remove* some types of PRs from your changelog by passing the
`--tags` parameter in the CLI. This is a list of a subset of names taken from the
left-most column above.
```

### Pull Requests with Multiple Matching Labels

If a pull request has multiple labels that match different categories, it will appear in **only the first matching section** based on the order of categories processed. For example, a PR labeled with both `api-change` and `enhancement` will appear only in the "API and Breaking Changes" section, not in "Enhancements made". The categories are processed in the same order as they show above.

## Include Pull Request reviewers and commenters in your changelog

By default, GitHub Activity will include anybody that _reviews_ or _comments_ in a pull request in the item for that PR. This is included in a list of authors at the end of each item. See [the JupyterHub Changelog](https://jupyterhub.readthedocs.io/en/stable/reference/changelog.html) for examples.

## Include a list of all contributors at the end of your changelog

By default, this tool will include a long list of contributors at the end of your changelog. This is the unique set of all contributors that contributed to the release.

(how-does-this-tool-define-contributions-in-the-reports)=

### How we define contributors in a changelog

GitHub Activity tries to automatically determine the unique list of contributors within a given window of time.
There are many ways to define this, and there isn't necessarily a "correct" method out there.

We try to balance the two extremes of "anybody who shows up is recognized as contributing" and "nobody is recognized as contributing".
We've chosen a few rules that try to reflect sustained engagement in issues/PRs, or contributions in the form of help in _others'_ issues or contributing code.

Here are the rules we follow for finding a list of contributors within a time window. A contributor is anyone who has:

- Contributed to a PR merged in that window (includes opening, merging, committing, or commenting)
- Commented on >= 2 issues that weren't theirs
- Commented >= 6 times on any one issue
- Known bot accounts are generally not considered contributors

We'd love feedback on whether this is a good set of rules to use.

## Strip PR type metadata from the changelog titles

If you follow the [title prefix convention used to split PRs](#prefixes-and-tags), you can remove these prefixes when you generate your changelog, so that they don't clutter the output.

To strip title prefix metadata, use the `--strip-brackets` flag.

For example, `[DOC] Add some documentation` will be rendered as `Add some documentation`.

## Change the heading level for your changelog items

To change the starting heading level for changelog items, use the `--heading-level N` flag. Where `N` is the starting heading level (e.g., `2` corresponds to `##`).

This is useful if you want to _embed_ your changelog into a larger one (e.g., `CHANGELOG.md`).

## Include issues in your changelog

To include closed issues in your changelog, use the `--include-issues` flag.

## Include opened issues in your changelog

To include Issues and Pull Requests that were _opened_ in a time period, use the `--include-opened` flag.

(use:token)=

## Remove bots from the changelog

`github-activity` automatically detects and excludes bot accounts using GitHub's API.
Bot accounts (like `dependabot`, `github-actions`, etc.) are identified by their account type in GitHub's data.

To ignore additional human contributors from the changelog, use the `--ignore-contributor` flag:

```
github-activity ... --ignore-contributor user-one --ignore-contributor 'test-user-*'
```

Wildcards are matched as per [filename matching semantics](https://docs.python.org/3/library/fnmatch.html#fnmatch.fnmatch).

## Use a GitHub API token

`github-activity` uses the GitHub API to pull information about a repository's activity.
You will quickly hit your API limit so you must use a personal access or API token.
There are two ways that you can generate your own access token for use with `github-activity`, each is described below:

### Create a token using the GitHub CLI

You can use [the GitHub command line interface](https://cli.github.com/manual/) to authenticate your account and store an access token in your local environment.
To do so, download the GitHub CLI, and run the following command:

```bash
# Authenticate with GitHub via the web interface
gh auth login --web
```

This will open a web interface for you to authenticate.
When finished, it will store an access token locally, which you can print with:

```bash
# Print an access token if it is stored
gh auth status -t
```

This token will automatically be used by `github-activity` if it exists.

### Manually create your own API token

Alternatively, you can create your own GitHub access token and store it yourself.
To do so, follow these steps:

- Create your own access token. Go to the [new GitHub access token page](https://github.com/settings/tokens/new) and follow the instructions.
  Note that while working with a public repository, you don't need to set any scopes on the token you create.
- Assign the token to an environment variable called `GITHUB_ACCESS_TOKEN` or `GITHUB_TOKEN`.
  If you run `github-activity` and this variable is defined, it will be used.
  You may also pass a token via the `--auth` parameter (though this is not the best security practice).

### Use the GitHub token in a GitHub Action

By default, `github-activity` will check for a variable called `GITHUB_TOKEN`, which exists for each repository in the GitHub Action. To over-ride this and use your personal token:

1. Set a repository secret with a name like `GHA_TOKEN`.
2. In your GitHub Workflow configuration, rename the token to `GITHUB_ACCESS_TOKEN` so that it over-rides the default `GITHUB_TOKEN` configuration.

For example:

```{code-block} yaml
jobs:
  tests:
    runs-on: ubuntu-24.04
    env:
      # This is a private access token for @choldgraf that has public read-only access.
      # FUTURE: We should update the tests to only pull from this repository and not
      # need a token at all.
      GITHUB_ACCESS_TOKEN: "${{ secrets.GHA_TOKEN }}"
```

## Use the Python API

You can do most of the above from Python as well.
This is not as well-documented as the CLI, but should have most functionality available.

### Generate markdown changelogs with the Python API

For generating markdown changelogs from Python, here's an example:

```
from github_activity import generate_activity_md

markdown = generate_activity_md(
    target="executablebooks/github-activity",
    since="2023-01-01",
    until="2023-12-31",
    kind=None,
    auth="your-github-token",
    tags=None,
    include_issues=True,
    include_opened=True,
    strip_brackets=True,
    heading_level=1,
    branch=None,
)

# Print or save the markdown
print(markdown)
```

### Return GitHub Activity queries as a DataFrame

For scraping GitHub and returning the data as a DataFrame, here's an example:

```python
from github_activity import get_activity

# Get activity data as a DataFrame
from github_activity import get_activity

df = get_activity(
    target="executablebooks/github-activity",
    since="2023-01-01",
    until="2023-12-31",
    auth="your-github-token",
    kind=None,
    cache=None
)
```

In some cases, metadata will be nested inside the resulting dataframe.
There are some helper functions for this. For example, to extract nested comments inside the activity dataframe:

```python
from github_activity import get_activity, extract_comments

df = get_activity(...)
comments_df = extract_comments(df['comments'])
```
