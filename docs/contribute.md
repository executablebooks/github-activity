# Contributor guide

These sections describe how you can make contributions to this theme.

## Run the tests

The easiest way to run the test suite is using [`nox`](https://nox.readthedocs.io/).
This will install the local version of the package and run the test suite.

```bash
nox -s test
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
