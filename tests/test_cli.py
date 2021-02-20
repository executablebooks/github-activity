from subprocess import run
from pathlib import Path


def test_cli(tmpdir, file_regression):
    path_tmp = Path(tmpdir)
    path_output = path_tmp.joinpath("out.md")

    url = "https://github.com/executablebooks/github-activity"
    org, repo = ("executablebooks", "github-activity")

    # CLI with URL
    cmd = f"github-activity {url} -s 2019-09-01 -u 2019-11-01 -o {path_output}"
    out = run(cmd.split(), check=True)
    md = path_output.read_text()
    file_regression.check(md, extension=".md")

    # CLI with parts
    cmd = f"github-activity {org}/{repo} -s 2019-09-01 -u 2019-11-01 -o {path_output}"
    out = run(cmd.split(), check=True)
    md = path_output.read_text()
    file_regression.check(md, extension=".md")

    # CLI with default branch
    cmd = f"github-activity {org}/{repo} -s 2019-09-01 -u 2019-11-01 -o {path_output} -b master"
    out = run(cmd.split(), check=True)
    md = path_output.read_text()
    file_regression.check(md, extension=".md")

    # CLI with non-existent branch
    cmd = f"github-activity {org}/{repo} -s 2019-09-01 -u 2019-11-01 -o {path_output} -b foo"
    out = run(cmd.split(), check=True)
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
    out = run(cmd.split(), check=True)
    md = path_output.read_text()
    md = md.split("## Contributors to this release")[0]
    file_regression.check(md, extension=".md")
