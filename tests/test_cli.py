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

    url = "https://github.com/executablebooks/jupyter-book"

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


def test_release_notes(tmpdir, file_regression):
    """Release notes that are automatically pulled from PR descriptions."""
    path_tmp = Path(tmpdir)
    path_output = path_tmp.joinpath("out.md")
    url = "https://github.com/executablebooks/jupyter-book"

    # This release range covers PRs with
    cmd = f"github-activity {url} -s v0.7.1 -u v0.7.3 --include-release-notes -o {path_output}"

    run(cmd.split(), check=True)

    md = path_output.read_text()
    test_md = md[md.index("## New features added") : md.index("## Bugs fixed")]
    file_regression.check(test_md, extension=".md")
