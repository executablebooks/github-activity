# Contributor guide

These sections describe how you can make contributions to this theme.

## Run the tests

The easiest way to run the test suite is using [`nox`](https://nox.readthedocs.io/).
This will install the local version of the package and run the test suite.

```bash
nox -s test
```

The tests don't call the GitHub API.
Instead they replay responses recorded with [`pytest-recording`](https://github.com/kiwicom/pytest-recording), which are stored in `tests/cassettes/`.

If you change the requests github-activity makes, the tests will fail with `CannotOverwriteExistingCassetteException`.
Re-record the cassettes with a GitHub token (read-only access to public repositories is enough) and commit them:

```bash
GITHUB_ACCESS_TOKEN=... nox -s test -- --record-mode=rewrite
```

Tokens are filtered out of the recordings.

Because the cassettes can't show changes on GitHub's side, the `live-api` workflow also runs the tests against the real GitHub API once a week.
To do the same locally, run:

```bash
GITHUB_ACCESS_TOKEN=... GITHUB_ACTIVITY_LIVE_TESTS=1 nox -s test
```

## Build the documentation

The easiest way to build the documentation locally is using `nox`.
To do so, run this command:

```bash
nox -s docs
```

To build the documentation with a liveserver that will automatically reload to show previews of your changes, use:

```bash
nox -s docs -- live
```

## Make a release

The easiest way to make a release is to follow these steps:

1. **Install `tbump`**:

   ```
   pip install tbump
   ```

1. **Bump the version**:

   ```
   tbump NEW_VERSION
   ```

   Then follow the prompts.

   This will bump the appropriate locations, make a release commit, and push the tag to GitHub.

1. **Generate a changelog for the new version**:

   ```
   github-activity -s [old-tag] -u [new-tag]
   ```

   We will paste this into the GitHub release.

1. **Draft a new release on GitHub**.
   Under the [`releases` page](https://github.com/executablebooks/github-activity/releases) click [the `Draft a New Release` button](https://github.com/executablebooks/github-activity/releases/new).
   - Connect the release to the tag you just pushed.
   - The name of the release is also `tag-name`.
   - Paste your changelog here.
1. **Publish the release**.
   When you hit `Publish release`, a GitHub action will trigger that runs our tests, and then publishes the latest tag to PyPI if the tests pass.
   That's it, you're done!
