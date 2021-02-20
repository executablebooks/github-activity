# github-activity

Generate simple markdown changelogs for GitHub repositories written in Python.

This package does two things:

1. Given a GitHub org, repository, an initial git reference or date, use the
   [GitHub GraphQL API](https://developer.github.com/v4/) to return a DataFrame
   of all issue and PR activity for this time period.
2. A CLI to render this activity as markdown, suitable for generating changelogs or
   community updates.

```{warning}
This is a really young tool so it might change a bit over time.
```

## Installation

The easiest way to install this package is to do so directly from GitHub with `pip`:

```
pip install git+https://github.com/choldgraf/github-activity
```

## Generate a markdown changelog

The easiest way to use `github-activity` to generate activity markdown is to use
the command-line interface. It takes the following form:

```
github-activity <org>/<repo> --since <date or ref> --until <date or ref>
```

The (optional) arguments in `--since` (or `-s`) and `--until` (or `-u`) can either be
a date, or a ref (such as a commit hash or tag). `github-activity` will pull the activity
between the dates corresponding to these values.

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

### Splitting PRs by tags and prefixes

Often you wish to split your PRs into multiple categories so that they are easier
to scan and parse. You may also *only* want to keep some PRs (e.g. features, or API
changes) while excluding others from your changelog.

`github-activity` uses the GitHub tags as well as PR prefixes to automatically
categorize each PR and display it in a section in your markdown. It roughly
follows the [keepachangelog taxonomy of changes](https://keepachangelog.com/en/1.0.0/).

Below is a list of the supported PR types, as well as the tags / title prefixes
that will be used to identify the right category.

```{include} tags_list.txt
```

```{tip}
You can choose to *remove* some types of PRs from your changelog by passing the
`--tags` parameter in the CLI. This is a list of a subset of names taken from the
left-most column above.
```

### Using a GitHub API token

`github-activity` uses the GitHub API to pull information about a repository's activity.
You will quickly hit your API limit unless you use a personal access token. Here are
instructions to generate and use a GitHub access token for use with `github-activity`.

* Create your own access token. Go to the [new GitHub access token page](https://github.com/settings/tokens/new)
  and follow the instructions. Note that while working with a public repository,
  you don't need to set any scopes on the token you create.
* When using `github-activity` from the command line, use the `--auth` parameter and pass
  in your access token. This is easiest if you set it as an **environment variable**,
  such as `MY_ACCESS_TOKEN`. You can then add it to your call like so:

  ```
  github-activity jupyter/notebook --since v2019-09-01 --auth $MY_ACCESS_TOKEN
  ```
* If you do not explicitly pass an access token to `github-activity`, it will search
  for an environment variable called `GITHUB_ACCESS_TOKEN`. If it finds this variable,
  it will use this in the API calls to GitHub.


## How does this tool define contributions in the reports?

GitHub Activity tries to automatically determine the unique list of contributors within
a given window of time. There are many ways to define this, and there isn't necessarily a
"correct" method out there.

We try to balance the two extremes of "anybody who shows up is recognized as contributing"
and "nobody is recognized as contributing". We've chosen a few rules that try to reflect
sustained engagement in issues/PRs, or contributions in the form of help in *others'* issues
or contributing code.

Here are the rules we follow for finding a list of contributors within a time window. A
contributor is anyone who has:

* Had their PR merged in that window
* Commented on >= 2 issues that weren't theirs
* Commented >= 6 times on any one issue

We'd love feedback on whether this is a good set of rules to use.
