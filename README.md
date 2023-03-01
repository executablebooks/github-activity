# github-activity

Generate simple markdown changelogs for GitHub repositories written in Python.

This package provides a CLI to do two things:

**Scrape all GitHub activity over a period of time for a repository**.
Given a GitHub org, repository, an initial git reference or date, use the [GitHub GraphQL API](https://developer.github.com/v4/) to return a DataFrame of all issue and PR activity for this time period.

**Render this as a markdwon changelog**.
Convert this DataFrame to markdown that is suitable for generating changelogs or   community updates.

For an example, see the [changelog of this package]([https://](https://github-activity.readthedocs.io/en/latest/changelog)).

## Use this tool

Use this tool via the command line like so:

```bash
github-activity [<org>/<repo>] --since <date or ref> --until <date or ref>
```

See [the User Guide for details on how to install and use this tool](https://github-activity.readthedocs.io/en/latest/use).

## Contribute to this package

See [the Contributing Guide for more details](https://github-activity.readthedocs.io/en/latest/contribute).
