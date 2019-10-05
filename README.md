# github-activity

A tool to generate simple markdown changelogs for GitHub repositories written in Python.

This package does two things:

1. Given a GitHub org, repository, and start date, use the [GitHub GraphQL
   API](https://developer.github.com/v4/) to return a DataFrame of all issue and
   PR activity for this time period.
2. Render this activity as markdown, suitable for generating changelogs or
   community updates.


## Installation

The easiest way to install this package is to do so directly from GitHub with `pip`:

```
pip install git+https://github.com/choldgraf/github-activity
```

## Usage

`gitlab-activity` use of the GitHub API require you to set a
`GITHUB_ACCESS_TOKEN` environment variable before use. To create one for use, go
[here](https://github.com/settings/tokens/new), and note that while working with
a public repository, you don't need to set any scopes on the token you create.

The easiest way to use github-activity to generate activity markdown is to use
the command-line interface. Here's an example on the
[jupyter notebook repository](https://github.com/jupyter/notebook), grabbing all
activity since September 2019 and outputting it to a markdown file.

```
github-activity jupyter/notebook 2019-09-01 -o notebook_activity.md
```

You can find the [resulting markdown here](docs/notebook_activity.md).

## Notes

* This is a really young tool so it might change a bit over time.
* You should really use a GitHub API token before running queries, as this will
  chew up your rate limit quickly otherwise.