# github-activity

Generate simple markdown changelogs for GitHub repositories written in Python.

This package does two things:

1. Given a GitHub org, repository, an initial git reference or date, use the
   [GitHub GraphQL API](https://developer.github.com/v4/) to return a DataFrame
   of all issue and PR activity for this time period.
2. A CLI to render this activity as markdown, suitable for generating changelogs or
   community updates.

## Installation

The easiest way to install this package is to do so directly from GitHub with `pip`:

```
pip install github-activity
```

```{toctree}
use
contribute
changelog
```

## How we define contributors in the reports

GitHub Activity tries to automatically determine the unique list of contributors within a given window of time.
There are many ways to define this, and there isn't necessarily a "correct" method out there.

We try to balance the two extremes of "anybody who shows up is recognized as contributing" and "nobody is recognized as contributing".
We've chosen a few rules that try to reflect sustained engagement in issues/PRs, or contributions in the form of help in _others'_ issues or contributing code.

Here are the rules we follow for finding a list of contributors within a time window. A contributor is anyone who has:

- Contributed to a PR merged in that window (includes opening, merging, committing, commenting, or committing)
- Commented on >= 2 issues that weren't theirs
- Commented >= 6 times on any one issue
- Known bot accounts are generally not considered contributors

We'd love feedback on whether this is a good set of rules to use.
