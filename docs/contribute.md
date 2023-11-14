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

1. **Bump the version in `__init__.py` and push it to master**.
   We try to use [semver version numbers](https://semver.org/) but don't stress out about it too much.
   - In your commit message use something like `RLS: vX.Y.Z`.
   - Add a changelog to `CHANGELOG.md`[^1].
2. **Draft a new release on GitHub**.
   Under the [`releases` page](https://github.com/executablebooks/github-activity/releases) click [the `Draft a New Release` button](https://github.com/executablebooks/github-activity/releases/new).
   - Connect the release to your release commit.
   - Create a new tag for the release called `vX.Y.Z`.
   - The name of the release is also `vM.m.p`.
   - Re-paste your changelog here as well if you like.
3. **Publish the release**.
   When you hit `Publish release`, a GitHub action will trigger that runs our tests, and then publishes the latest tag to PyPI if the tests pass.
   That's it, you're done!

[^1]: To add a changelog with `github-activity`, run something like:

    ```bash
    github-activity -s <LAST-TAG> -o tmp.md
    ```

    Then copy the contents of `tmp.md` and paste it into our changelog, bumping section header levels if needed.
    Alternatively, use `nox`:

    ```bash
    nox -s changelog
    ```
