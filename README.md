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

See [the github-activity documentation](https://github-activity.readthedocs.io)
for more information.
