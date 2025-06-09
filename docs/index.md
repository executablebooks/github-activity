# github-activity

Generate markdown changelogs for GitHub repositories with more control over the kinds of contributions that are included.

GitHub Activity allows you to include more than just "PR author" in your changelogs, such as PR reviewers and issue commenters. This allows you to give credit to a wider group of contributors around your project. Below are some examples, see [](#how-does-this-tool-define-contributions-in-the-reports) for more information.

- PR Authors
- PR Reviewers and Mergers
- Issue and PR commenters

It also allows you split PRs into sections in your changelog, using either PR labels or PR title metadata (e.g., `[ENH]`). See [](#prefixes-and-tags) for more information.

GitHub Activity uses the [GitHub GraphQL API](https://docs.github.com/en/graphql), along with some basic pagination and caching to efficiently pull data from GitHub.

```{seealso}
See [the JupyterHub Team changelog](https://github.com/jupyterhub/jupyterhub/blob/5.3.0/docs/source/reference/changelog.md) for an example of this tool in action.
```

## Installation and basic usage

The easiest way to install this package is to do so directly from GitHub with `pip`:

```bash
pip install github-activity
```

You can then use it like so:

```bash
github-activity [<org>/<repo>] --since <date or ref> --until <date or ref>
```

## Why use this tool?

We created `github-activity` because there is a lot that goes into building open source tools than just making a pull request. This tool tries to surface more diverse contributions around a release, like reviews, comments, etc. It tries to paint a more complete picture of all the work that goes into building open source software.

You might want to use this tool if you're hoping to give credit and attribution to more people in your open source community. This gives your community a feeling of more appreciation, and can create more incentives for others to contribute.

```{toctree}
:maxdepth: 2
use
contribute
changelog
```
