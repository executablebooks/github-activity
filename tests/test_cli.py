import os
import shutil
from pathlib import Path
from subprocess import run

from pytest import mark


@mark.parametrize(
    "cmd,basename",
    [
        # CLI with URL
        (
            "github-activity {url} -s 2019-09-01 -u 2019-11-01 -o {path_output}",
            "cli_w_url",
        ),
        # CLI with parts
        (
            "github-activity {org}/{repo} -s 2019-09-01 -u 2019-11-01 -o {path_output}",
            "cli_w_parts",
        ),
        # CLI with default branch
        (
            "github-activity {org}/{repo} -s 2019-09-01 -u 2019-11-01 -o {path_output} -b master",
            "cli_def_branch",
        ),
        # CLI with no target
        (
            "github-activity -s 2019-09-01 -u 2019-11-01 -o {path_output}",
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
    cmd = "github-activity -s 2019-09-01 -u 2019-11-01 -o {path_output}"
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

    cmd = f"github-activity {org}/{repo} -s 2019-09-01 -u 2019-11-01 -o {path_output} -b foo"
    run(cmd.split(), check=True)
    md = path_output.read_text()
    assert "Contributors to this release" in md
    assert "Merged PRs" not in md


def test_pr_split(tmpdir, file_regression):
    """Test that PRs are properly split by tags/prefixes."""
    path_tmp = Path(tmpdir)
    path_output = path_tmp.joinpath("out.md")

    url = "https://github.com/jupyter-book/jupyter-book"

    # This release range covers some PRs with tags, and some with prefixes
    cmd = f"github-activity {url} -s v0.7.1 -u v0.7.3 -o {path_output}"
    run(cmd.split(), check=True)
    md = path_output.read_text()
    md = md.split("## Contributors to this release")[0]
    file_regression.check(md, extension=".md")


def test_cli_all(tmpdir, file_regression):
    """Test that a full changelog is created"""
    path_tmp = Path(tmpdir)
    path_output = path_tmp.joinpath("out.md")
    cmd = f"github-activity executablebooks/github-activity --all -o {path_output}"
    run(cmd.split(), check=True)
    md = path_output.read_text()
    index = md.index("## v0.2.0")
    file_regression.check(md[index:], extension=".md")
