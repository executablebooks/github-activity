# github-activity

Generate markdown changelogs for GitHub repositories with more control over the kinds of contributions that are included.

GitHub Activity allows you to include more than just "PR author" in your changelogs, such as PR reviewers and issue commenters. This allows you to give credit to a wider group of contributors around your project.

```{seealso}
See [the JupyterHub Team changelog](https://github.com/jupyterhub/jupyterhub/blob/5.3.0/docs/source/reference/changelog.md) for an example of this tool in action.
```

```{toctree}
use
contribute
changelog
```

## Installation

The easiest way to install this package is to do so directly from GitHub with `pip`:

```
pip install github-activity
```

## Why does this tool exist?

We created `github-activity` because there is a lot that goes into building open source tools than just making a pull request. This tool tries to surface more diverse contributions around a release, like reviews, comments, etc. It tries to paint a more complete picture of all the work that goes into building open source software.

You might want to use this tool if you're hoping to give credit and attribution to more people in your open source community. This gives your community a feeling of more appreciation, can create more incentives for others to contribute.
