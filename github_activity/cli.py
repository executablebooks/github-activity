import argparse
import os
import sys

from .github_activity import generate_activity_md

DESCRIPTION = "Generate a markdown changelog of GitHub activity within a date window."
parser = argparse.ArgumentParser(description=DESCRIPTION)
parser.add_argument(
    "target",
    help="""The GitHub organization/repo for which you want to grab recent issues/PRs.
    Can either be *just* an organization (e.g., `jupyter`), or a combination
    organization and repo (e.g., `jupyter/notebook`). If the former, all
    repositories for that org will be used. If the latter, only the specified
    repository will be used. Can also be a GitHub URL to an organization or repo.""",
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
        "variable `GITHUB_ACCESS_TOKEN` will be tried."
    ),
)
parser.add_argument(
    "--tags",
    default=None,
    help=(
        "A list of the tags to use in generating subsets of PRs for the "
        "markdown report. Must be one of:"
        ""
        "   ['enhancement', 'bugs', 'maintenance', 'documentation', 'api_change']"
        ""
        "If None, all of the above tags will be used."
    ),
)
parser.add_argument(
    "--include-issues",
    default=False,
    action="store_true",
    help="Include Issues in the markdown output",
)
parser.add_argument(
    "--include-opened",
    default=False,
    action="store_true",
    help="Include a list of opened items in the markdown output",
)
parser.add_argument(
    "--strip-brackets",
    default=False,
    action="store_true",
    help=(
        "If True, strip any text between brackets at the beginning of the issue/PR title. "
        "E.g., [MRG], [DOC], etc."
    ),
)


def main():
    args = parser.parse_args(sys.argv[1:])
    tags = args.tags.split(",") if args.tags is not None else args.tags
    md = generate_activity_md(
        args.target,
        since=args.since,
        until=args.until,
        kind=args.kind,
        auth=args.auth,
        tags=tags,
        include_issues=bool(args.include_issues),
        include_opened=bool(args.include_opened),
        strip_brackets=bool(args.strip_brackets),
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
        print(f"Finished writing markdown to: {args.output}")
    else:
        print(md)


if __name__ == "__main__":
    main()
