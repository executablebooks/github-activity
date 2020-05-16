from subprocess import run
from pathlib import Path


def test_cli(tmpdir, file_regression):
    path_tmp = Path(tmpdir)
    path_output = path_tmp.joinpath("out.md")

    url = "https://github.com/choldgraf/github-activity"
    org, repo = ("choldgraf", "github-activity")

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


def test_tags(tmpdir, file_regression):
    path_tmp = Path(tmpdir)
    path_output = path_tmp.joinpath("out.md")

    url = "https://github.com/executablebooks/sphinx-book-theme"

    # CLI with URL
    cmd = f"github-activity {url} -s v0.0.2 -u v0.0.4 -o {path_output}"
    out = run(cmd.split(), check=True)
    md = path_output.read_text()
    file_regression.check(md, extension=".md")
