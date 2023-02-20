import nox

nox.options.reuse_existing_virtualenvs = True


@nox.session
def run(session):
    """Run github activity on this repository with the current repo."""
    session.install("-r", "requirements.txt")
    session.install("-e", ".")

    # Run github activity and re-use the posargs
    cmd = ["github-activity"] + session.posargs
    session.run(*cmd)
