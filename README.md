# github-activity

Generate simple markdown changelogs for GitHub repositories written in Python.

This package does two things:

1. Given a GitHub org, repository, an initial git reference or date, use the
   [GitHub GraphQL API](https://developer.github.com/v4/) to return a DataFrame
   of all issue and PR activity for this time period.
2. A CLI to render this activity as markdown, suitable for generating changelogs or
   community updates.

*Note: This is a really young tool so it might change a bit over time.*

## Installation

The easiest way to install this package is to do so directly from GitHub with `pip`:

```
pip install git+https://github.com/choldgraf/github-activity
```

## Usage

The easiest way to use `github-activity` to generate activity markdown is to use
the command-line interface. It takes the following form:

```
github-activity <org>/<repo> --since <date or ref> --until <date or ref>
```

The (optional) arguments in `--since` and `--until` can either be a date, or
a ref (such as a commit hash or tag). `github-activity` will pull the activity
between the dates corresponding to these values.

Here's an example on the
[jupyter notebook repository](https://github.com/jupyter/notebook), grabbing all
activity since the latest major release and outputting it to a markdown file.

```
github-activity jupyter/notebook --since 6.0.0 -o docs/notebook_activity.md
```

You can find the [resulting markdown here](docs/notebook_activity.md).

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
