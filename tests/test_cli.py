from pathlib import Path
from subprocess import run


def test_cli(tmpdir, file_regression):
    """The output of all file_regressions should be the same, testing diff opts."""
    path_tmp = Path(tmpdir)
    path_output = path_tmp.joinpath("out.md")

    url = "https://github.com/executablebooks/github-activity"
    org, repo = ("executablebooks", "github-activity")

    # CLI with URL
    cmd = f"github-activity {url} -s 2019-09-01 -u 2019-11-01 -o {path_output}"
    run(cmd.split(), check=True)
    md = path_output.read_text()
    file_regression.check(md, basename="cli_w_url", extension=".md")

    # CLI with parts
    cmd = f"github-activity {org}/{repo} -s 2019-09-01 -u 2019-11-01 -o {path_output}"
    run(cmd.split(), check=True)
    md = path_output.read_text()
    file_regression.check(md, basename="cli_w_parts", extension=".md")

    # CLI with default branch
    cmd = f"github-activity {org}/{repo} -s 2019-09-01 -u 2019-11-01 -o {path_output} -b master"
    run(cmd.split(), check=True)
    md = path_output.read_text()
    file_regression.check(md, basename="cli_def_branch", extension=".md")

    # CLI with non-existent branch
    cmd = f"github-activity {org}/{repo} -s 2019-09-01 -u 2019-11-01 -o {path_output} -b foo"
    run(cmd.split(), check=True)
    md = path_output.read_text()
    assert "Contributors to this release" in md
    assert "Merged PRs" not in md

    # CLI with no target
    cmd = f"github-activity -s 2019-09-01 -u 2019-11-01 -o {path_output}"
    run(cmd.split(), check=True)
    md = path_output.read_text()
    file_regression.check(md, basename="cli_no_target", extension=".md")


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
