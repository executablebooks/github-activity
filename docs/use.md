# User guide

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

### Split PRs by tags and prefixes

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

(use:token)=

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
- Assign the token to an environment variable called `GITHUB_ACCESS_TOKEN`.
  If you run `github-activity` and this variable is defined, it will be used.
  You may also pass a token via the `--auth` parameter (though this is not the best security practice).
