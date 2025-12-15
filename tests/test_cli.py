import shutil
from pathlib import Path
from subprocess import run

from pytest import mark


@mark.parametrize(
    "cmd,basename",
    [
        # CLI with URL
        (
            "github-activity {url} -s 2021-01-01 -u 2021-01-15 -o {path_output}",
            "cli_w_url",
        ),
        # CLI with parts
        (
            "github-activity {org}/{repo} -s 2021-01-01 -u 2021-01-15 -o {path_output}",
            "cli_w_parts",
        ),
        # CLI with explicit branch filter (using master since that was likely the name in 2021)
        (
            "github-activity {org}/{repo} -s 2021-01-01 -u 2021-01-15 -o {path_output} -b master",
            "cli_def_branch",
        ),
        # CLI with no target
        (
            "github-activity -s 2021-01-01 -u 2021-01-15 -o {path_output}",
            "cli_no_target",
        ),
    ],
)
def test_cli(tmpdir, file_regression, cmd, basename):
    """The output of all file_regressions should be the same, testing diff opts."""
    path_tmp = Path(tmpdir)
    path_output = path_tmp.joinpath("out.md")

    url = "https://github.com/executablebooks/github-activity"
    org, repo = ("executablebooks", "github-activity")

    command = cmd.format(path_output=path_output, url=url, org=org, repo=repo)
    run(command.split(), check=True)
    md = path_output.read_text()
    file_regression.check(md, basename=basename, extension=".md")


def test_cli_dot_config(tmp_path, monkeypatch, file_regression):
    """Test that pyproject.toml config is loaded"""
    cmd = "github-activity -s 2021-01-01 -u 2021-01-15 -o {path_output}"
    basename = "cli_no_target_pyproject"

    path_output = tmp_path / "out.md"

    # We need to augment the repository with a custom .githubactivity.json
    # but since a local git repo is only needed to get the origin a shallow
    # clone is enough
    run(
        [
            "git",
            "clone",
            "--depth=1",
            "https://github.com/executablebooks/github-activity",
            str(tmp_path / "repo"),
        ],
        check=True,
    )
    tests_dir = Path(__file__).parent
    shutil.copyfile(
        str(tests_dir / "resources" / "cli_no_target.githubactivity.json"),
        str(tmp_path / "repo" / ".githubactivity.json"),
    )

    # cd into a subdirectory so we test the lookup of .githubactivity.json
    monkeypatch.chdir(tmp_path / "repo" / "tests")

    command = cmd.format(path_output=path_output)
    run(command.split(), check=True)
    md = path_output.read_text()
    file_regression.check(md, basename=basename, extension=".md")


def test_cli_nonexistent_branch(tmpdir):
    path_tmp = Path(tmpdir)
    path_output = path_tmp.joinpath("out.md")

    org, repo = ("executablebooks", "github-activity")

    cmd = f"github-activity {org}/{repo} -s 2021-01-01 -u 2021-01-15 -o {path_output} -b foo"
    run(cmd.split(), check=True)
    md = path_output.read_text()
    assert "Contributors to this release" in md
    assert "Merged PRs" not in md


def test_pr_split(tmpdir, file_regression):
    """Test that PRs are properly split by tags/prefixes."""
    path_tmp = Path(tmpdir)
    path_output = path_tmp.joinpath("out.md")

    url = "https://github.com/executablebooks/github-activity"

    # Test PR tag/prefix splitting using recent consecutive releases
    cmd = f"github-activity {url} -s v1.0.2 -u v1.0.3 -o {path_output}"
    run(cmd.split(), check=True)
    md = path_output.read_text()
    md = md.split("## Contributors to this release")[0]
    file_regression.check(md, extension=".md")


def test_cli_all(tmpdir, file_regression):
    """Test that a full changelog is created"""
    path_tmp = Path(tmpdir)
    path_output = path_tmp.joinpath("out.md")
    # Use recent consecutive releases to reduce API calls
    cmd = f"github-activity executablebooks/github-activity -s v1.0.2 -u v1.0.3 -o {path_output}"
    run(cmd.split(), check=True)
    md = path_output.read_text()
    file_regression.check(md, extension=".md")


def test_cli_ignore_user(tmpdir):
    """Test that a full changelog is created"""
    path_tmp = Path(tmpdir)
    path_output = path_tmp.joinpath("out.md")
    # Add end date to limit query range
    cmd = f"github-activity executablebooks/github-activity --ignore-contributor choldgraf -s v1.0.2 -u v1.0.3 -o {path_output}"
    run(cmd.split(), check=True)
    md = path_output.read_text()
    assert "@choldgraf" not in md


def test_contributor_sorting(tmpdir, file_regression):
    """Test that PR author appears first, then rest of contributors, sorted"""
    path_tmp = Path(tmpdir)
    path_output = path_tmp.joinpath("out.md")

    org, repo = ("executablebooks", "github-activity")

    # Test contributor sorting using recent consecutive releases
    cmd = f"github-activity {org}/{repo} -s v0.2.0 -u v0.3.0 -o {path_output}"
    run(cmd.split(), check=True)
    md = path_output.read_text()
    file_regression.check(md, extension=".md")


@mark.integration
def test_bot_filtering(file_regression):
    """Test that bot users are detected and filtered from output."""
    from github_activity.github_activity import get_activity, generate_activity_md

    # Use jupyter-book/mystmd because it's a small release, and know theres bot activity
    data = get_activity(
        target="jupyter-book/mystmd",
        since="mystmd@1.6.5",
        until="mystmd@1.6.6",
    )

    # Verify bot_users attrs exists and was preserved (catches the concat bug)
    assert "bot_users" in data.attrs, "bot_users should be in DataFrame attrs"

    # Verify we actually detected some bots
    assert len(data.attrs["bot_users"]) > 0, (
        "Should have detected bot users in this release"
    )

    # Generate markdown and save as regression baseline
    md = generate_activity_md(
        target="jupyter-book/mystmd",
        since="mystmd@1.6.5",
        until="mystmd@1.6.6",
    )

    # Use this regression test to make sure no bots are in the output
    file_regression.check(md, extension=".md")
