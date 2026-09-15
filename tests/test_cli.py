import shutil
from pathlib import Path
from subprocess import run

from pytest import mark

from github_activity.cli import main

# GitHub API responses are replayed from tests/cassettes/, re-record them with:
#   GITHUB_ACCESS_TOKEN=... pytest --record-mode=rewrite
pytestmark = mark.vcr


@mark.parametrize(
    "cmd,basename",
    [
        # CLI with URL
        (
            "{url} -s 2021-01-01 -u 2021-01-15 -o {path_output}",
            "cli_w_url",
        ),
        # CLI with parts
        (
            "{org}/{repo} -s 2021-01-01 -u 2021-01-15 -o {path_output}",
            "cli_w_parts",
        ),
        # CLI with explicit branch filter (using master since that was likely the name in 2021)
        (
            "{org}/{repo} -s 2021-01-01 -u 2021-01-15 -o {path_output} -b master",
            "cli_def_branch",
        ),
        # CLI with no target
        (
            "-s 2021-01-01 -u 2021-01-15 -o {path_output}",
            "cli_no_target",
        ),
    ],
    # Short ids so the cassette file names stay readable
    ids=["cli_w_url", "cli_w_parts", "cli_def_branch", "cli_no_target"],
)
def test_cli(tmpdir, file_regression, cmd, basename):
    """The output of all file_regressions should be the same, testing diff opts."""
    path_tmp = Path(tmpdir)
    path_output = path_tmp.joinpath("out.md")

    url = "https://github.com/executablebooks/github-activity"
    org, repo = ("executablebooks", "github-activity")

    command = cmd.format(path_output=path_output, url=url, org=org, repo=repo)
    main(command.split())
    md = path_output.read_text()
    file_regression.check(md, basename=basename, extension=".md")


def test_cli_dot_config(tmp_path, monkeypatch, file_regression):
    """Test that pyproject.toml config is loaded"""
    cmd = "-s 2021-01-01 -u 2021-01-15 -o {path_output}"
    basename = "cli_no_target_pyproject"

    path_output = tmp_path / "out.md"

    # A local repository with an origin is enough to test config lookup.
    repo_path = tmp_path / "repo"
    (repo_path / "tests").mkdir(parents=True)
    run(["git", "init", str(repo_path)], check=True)
    run(
        [
            "git",
            "-C",
            str(repo_path),
            "remote",
            "add",
            "origin",
            "https://github.com/executablebooks/github-activity",
        ],
        check=True,
    )
    tests_dir = Path(__file__).parent
    shutil.copyfile(
        str(tests_dir / "resources" / "cli_no_target.githubactivity.json"),
        str(repo_path / ".githubactivity.json"),
    )

    # cd into a subdirectory so we test the lookup of .githubactivity.json
    monkeypatch.chdir(repo_path / "tests")

    command = cmd.format(path_output=path_output)
    main(command.split())
    md = path_output.read_text()
    file_regression.check(md, basename=basename, extension=".md")


def test_cli_nonexistent_branch(tmpdir):
    path_tmp = Path(tmpdir)
    path_output = path_tmp.joinpath("out.md")

    org, repo = ("executablebooks", "github-activity")

    cmd = f"{org}/{repo} -s 2021-01-01 -u 2021-01-15 -o {path_output} -b foo"
    main(cmd.split())
    md = path_output.read_text()
    assert "Contributors to this release" in md
    assert "Merged PRs" not in md


def test_changelog_features(file_regression):
    """Combined test for multiple changelog features to minimize API calls.

    This tests a few things in one regression test.
    """
    from github_activity.github_activity import generate_activity_md

    # This is a release that has dependabot activity, so we test that it no longer
    # shows up in the changelog. It *will* show up in the release below because it's
    # from before this feature was implemented.
    # ref: https://github.com/executablebooks/github-activity/releases/tag/v1.1.0
    org = "executablebooks"
    repo = "github-activity"
    since = "v1.0.2"
    until = "v1.1.0"

    # Test general changelog structure with a regression test
    # PRs should be split by issue label.
    md_full = generate_activity_md(
        target=f"{org}/{repo}",
        since=since,
        until=until,
        ignored_contributors=["choldgraf"],
    )
    file_regression.check(md_full, basename="test_cli_all", extension=".md")

    # Test that contributor sorting works, minus @choldgraf since we filtered him out (sorry Chris)
    assert (
        "- Allow excluding certain usernames from changelog [#128](https://github.com/executablebooks/github-activity/pull/128) ([@stefanv](https://github.com/stefanv), [@bsipocz](https://github.com/bsipocz), [@nabobalis](https://github.com/nabobalis))"
        in md_full
    ), "Contributors should be sorted as expected"

    # Test that ignored usernames are ignored
    assert "@choldgraf" not in md_full.lower(), (
        "Ignored contributor should not appear in output"
    )
    # Test that bots are removed
    assert "@dependabot" not in md_full.lower(), (
        "Bot user dependabot should not appear in output"
    )


def test_invalid_repository_error():
    """Test that invalid repository names produce clear error messages."""
    import pytest

    from github_activity.github_activity import get_activity

    # Test with an invalid repository name
    with pytest.raises(ValueError) as exc_info:
        get_activity(
            target="invalid-org/nonexistent-repo-12345",
            since="2021-01-01",
            until="2021-01-15",
        )

    # Verify the error message mentions the repository
    error_message = str(exc_info.value)
    assert "repository" in error_message.lower(), (
        f"Error should mention repository, got: {error_message}"
    )
    assert "invalid-org/nonexistent-repo-12345" in error_message, (
        f"Error should include the repo name, got: {error_message}"
    )
