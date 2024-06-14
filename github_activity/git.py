import subprocess


def _git_installed_check():
    cmd = ["git", "--help"]
    try:
        subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False


def _git_toplevel_path():
    """Fetch the top-level of the local Git repository"""
    cmd = ["git", "rev-parse", "--show-toplevel"]
    try:
        top = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
        return top.strip().decode()
    except subprocess.CalledProcessError:
        return None
