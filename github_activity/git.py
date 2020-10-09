import subprocess

def _git_installed_check():
    cmd = ["git", "--help"]
    try:
        subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False


def _valid_git_reference_check(git_ref):
    cmd = ["git", "rev-parse", "--verify", git_ref]
    try:
        subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False
