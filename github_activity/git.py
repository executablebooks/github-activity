import os.path
import re
import shlex
import subprocess
from tempfile import TemporaryDirectory
from typing import Dict, List, Tuple

def _git_installed_check() -> bool:
    cmd = ["git", "--help"]
    try:
        subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False


def _git_get_remotes() -> Dict[str, str]:
    out = subprocess.run("git remote -v".split(), stdout=subprocess.PIPE)
    remotes = out.stdout.decode().split("\n")
    remotes = [ii for ii in remotes if ii]
    return {
        ii.split("\t")[0]: ii.split("\t")[1].split()[0] for ii in remotes
    }


def _git_get_remote_sha_and_tags(repo: str, pattern: str) -> List[Tuple[str, str]]:
    # Get the sha and tag name for each tag in the target repo
    with TemporaryDirectory() as td:

        subprocess.run(
            shlex.split(f"git clone {repo} repo"), cwd=td
        )
        repo = os.path.join(td, "repo")
        subprocess.run(shlex.split("git fetch origin --tags"), cwd=repo)

        cmd = 'git log --tags --simplify-by-decoration --pretty="format:%h | %D"'
        data = (
            subprocess.check_output(shlex.split(cmd), cwd=repo)
            .decode("utf-8")
            .splitlines()
        )

    # Clean up the raw data
    pattern = f"tag: {pattern}"

    def filter(datum):
        _, tag = datum
        # Handle the HEAD tag if it exists
        if "," in tag:
            tag = tag.split(", ")[1]
        return re.match(pattern, tag) is not None

    data = [d.split(" | ") for (i, d) in enumerate(data)]
    return [d for d in data if filter(d)]