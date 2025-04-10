import nox

nox.options.reuse_existing_virtualenvs = True


@nox.session
def changelog(session):
    """Run github activity on this repository with the current repo."""
    session.install("-r", "requirements.txt")
    session.install("-e", ".")

    # Run github activity and re-use the posargs
    cmd = ["github-activity"] + session.posargs + ["-o", "tmp.md"]
    session.run(*cmd)


@nox.session
def docs(session):
    """Run github activity on this repository with the current repo."""
    session.install("-e", ".[sphinx]")
    session.install("-r", "docs/requirements.txt")

    if "live" in session.posargs:
        session.install("sphinx-autobuild")
        session.run(
            "sphinx-autobuild",
            "-b",
            "dirhtml",
            "--port",
            "0",
            "docs",
            "docs/_build/dirhtml",
        )
    else:
        session.run("sphinx-build", "-b", "dirhtml", "docs", "docs/_build/dirhtml")


@nox.session
def test(session):
    """Run github activity on this repository with the current repo."""
    session.install("-r", "requirements.txt")
    session.install("-e", ".[testing]")

    # Run github activity and re-use the posargs
    cmd = ["pytest", "--verbose", "--durations=10"] + session.posargs
    session.run(*cmd)
