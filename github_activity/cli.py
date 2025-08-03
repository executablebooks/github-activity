import argparse
import json
import os
import sys
from subprocess import PIPE
from subprocess import run

from .git import _git_installed_check
from .git import _git_toplevel_path
from .github_activity import _parse_target
from .github_activity import generate_activity_md
from .github_activity import generate_all_activity_md

DESCRIPTION = "Generate a markdown changelog of GitHub activity within a date window."

# These defaults are managed by load_config_and_defaults so that they can be
# overridden by a config file
ARG_DEFAULTS = {
    "heading-level": 1,
    "include-issues": False,
    "include-opened": False,
    "strip-brackets": False,
    "all": False,
    "ignore-contributor": [],
}

parser = argparse.ArgumentParser(description=DESCRIPTION)
parser.add_argument(
    "-t",
    "--target",
    nargs="?",
    default=None,
    help="""The GitHub organization/repo for which you want to grab recent issues/PRs.
    Can either be *just* an organization (e.g., `jupyter`), or a combination
    organization and repo (e.g., `jupyter/notebook`). If the former, all
    repositories for that org will be used. If the latter, only the specified
    repository will be used. Can also be a GitHub URL to an organization or repo. If
    None, the org/repo will attempt to be inferred from `git remote -v`.""",
)
parser.add_argument(
    "-s",
    "--since",
    nargs="?",
    default=None,
    help="""Return issues/PRs with activity since this date or git reference. Can be
    any string that is parsed with dateutil.parser.parse.""",
)
parser.add_argument(
    "-u",
    "--until",
    nargs="?",
    default=None,
    help="""Return issues/PRs with activity until this date or git reference. Can be
    any string that is parsed with dateutil.parser.parse. If none, today's
    date will be used.""",
)
parser.add_argument(
    "-o", "--output", default=None, help="""Write the markdown to a file if desired."""
)
parser.add_argument(
    "--kind",
    default=None,
    help="""Return only issues or PRs. If None, both will be returned.""",
)
parser.add_argument(
    "--auth",
    default=None,
    help=(
        "An authentication token for GitHub. If None, then the environment "
        "variable `GITHUB_ACCESS_TOKEN` will be tried. If it does not exist "
        "then attempt to infer the token from `gh auth status -t`."
    ),
)
parser.add_argument(
    "--tags",
    default=None,
    help=(
        "A list of the tags to use in generating subsets of PRs for the "
        "markdown report. Must be one of:"
        ""
        "   ['api_change', 'new', 'enhancement', 'bug', 'maintenance', 'documentation', 'ci', 'deprecate']"
        ""
        "If None, all of the above tags will be used."
    ),
)
parser.add_argument(
    "--include-issues",
    default=None,
    action="store_true",
    help="Include Issues in the markdown output",
)
parser.add_argument(
    "--include-opened",
    default=None,
    action="store_true",
    help="Include a list of opened items in the markdown output",
)
parser.add_argument(
    "--strip-brackets",
    default=None,
    action="store_true",
    help=(
        "If True, strip any text between brackets at the beginning of the issue/PR title. "
        "E.g., [MRG], [DOC], etc."
    ),
)
parser.add_argument(
    "--heading-level",
    default=None,
    type=int,
    help=(
        """Base heading level to add when generating markdown.

        Useful when including changelog output in an existing document.

        By default, changelog is emitted with one h1 and an h2 heading for each section.

        --heading-level=2 starts at h2, etc.
        """
    ),
)
parser.add_argument(
    "--branch",
    "-b",
    default=None,
    help=("""The branch or reference name to filter pull requests by"""),
)
parser.add_argument(
    "--all",
    default=None,
    action="store_true",
    help=("""Whether to include all the GitHub tags"""),
)
parser.add_argument(
    "--ignore-contributor",
    action="append",
    help="Do not include this GitHub username as a contributor in the changelog",
)

# Hidden argument so that target can be optionally passed as a positional argument
parser.add_argument(
    "_target",
    nargs="?",
    default=None,
    help=argparse.SUPPRESS,
)


def load_config_and_defaults(args):
    """
    Load .githubactivity.json from the Git top-level directory,
    override unset args with values from .githubactivity.json,
    and set defaults for remaining args.
    """
    config = {}
    git_toplevel = _git_toplevel_path()
    if git_toplevel:
        try:
            with open(os.path.join(git_toplevel, ".githubactivity.json")) as f:
                config = json.load(f)
        except FileNotFoundError:
            pass

    # Treat args as a dict
    # https://docs.python.org/3/library/argparse.html#the-namespace-object
    for argname in vars(args):
        configname = argname.replace("_", "-")
        if getattr(args, argname) is None:
            setattr(args, argname, config.get(configname, ARG_DEFAULTS.get(configname)))


def main():
    if not _git_installed_check():
        print("git is required to run github-activity", file=sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    if args.target and args._target:
        raise ValueError(
            "target cannot be passed as both a positional and keyword argument"
        )
    if not args.target:
        args.target = args._target

    load_config_and_defaults(args)

    tags = args.tags.split(",") if args.tags is not None else args.tags
    # Automatically detect the target from remotes if we haven't had one passed.
    if not args.target:
        err = "Could not automatically detect remote, and none was given."
        try:
            out = run("git remote -v".split(), stdout=PIPE)
            remotes = out.stdout.decode().split("\n")
            remotes = [ii for ii in remotes if ii]
            remotes = {
                ii.split("\t")[0]: ii.split("\t")[1].split()[0] for ii in remotes
            }
            if "upstream" in remotes:
                ref = remotes["upstream"]
            elif "origin" in remotes:
                ref = remotes["origin"]
            else:
                ref = None
            if not ref:
                raise ValueError(err)

            org, repo = _parse_target(ref)
            if repo:
                args.target = f"{org}/{repo}"
            else:
                args.target = f"{org}"
        except Exception:
            raise ValueError(err)

    common_kwargs = dict(
        kind=args.kind,
        auth=args.auth,
        tags=tags,
        include_issues=bool(args.include_issues),
        include_opened=bool(args.include_opened),
        strip_brackets=bool(args.strip_brackets),
        branch=args.branch,
        ignored_contributors=args.ignore_contributor,
    )

    if args.all:
        md = generate_all_activity_md(args.target, **common_kwargs)

    else:
        md = generate_activity_md(
            args.target,
            since=args.since,
            until=args.until,
            heading_level=args.heading_level,
            **common_kwargs,
        )

    if not md:
        return

    if args.output:
        output = os.path.abspath(args.output)
        output_dir = os.path.dirname(output)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        with open(args.output, "w") as ff:
            ff.write(md)
        print(f"Finished writing markdown to: {args.output}", file=sys.stderr)
    else:
        print(md)


if __name__ == "__main__":
    main()
