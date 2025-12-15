import os
import sys

import numpy as np
import pandas as pd
import requests
from tqdm.auto import tqdm

from .auth import TokenAuth

comments_query = """\
        comments(last: 100) {
          edges {
            node {
              authorAssociation
              createdAt
              updatedAt
              url
              author {
                login
                __typename
              }
            }
          }
        }
"""

reviews_query = """\
        reviews(last: 100) {
          edges {
            node {
              authorAssociation
              author {
                login
                __typename
              }
            }
          }
        }
"""

commits_query = """\
        commits(first: 100) {
          edges {
            node {
              commit {
                committer {
                  user {
                    login
                    __typename
                  }
                }
                authors(first: 10) {
                  edges {
                    node {
                      user {
                        login
                        __typename
                      }
                    }
                  }
                }
              }
            }
          }
        }
"""

base_elements = """\
        state
        id
        title
        url
        createdAt
        updatedAt
        closedAt
        labels(first: 10) {
            edges {
                node {
                    name
                }
            }
        }
        number
        authorAssociation
        author {
          login
          __typename
        }
        reactions(content: THUMBS_UP) {
          totalCount
        }
"""

gql_template = """\
{{
  search({query}) {{
    issueCount
    pageInfo {{
        endCursor
        hasNextPage
    }}
    nodes {{
      ... on PullRequest {{
        {base_elements}
        mergedBy {{
          login
          __typename
        }}
        mergeCommit {{
          oid
        }}
        baseRefName
        {comments}
        {commits}
        {reviews}
      }}
      ... on Issue {{
        {base_elements}
        {comments}
      }}
    }}
  }}
}}
"""


# Define our query object that we'll re-use for github search
class GitHubGraphQlQuery:
    def __init__(self, query, display_progress=True, auth=None):
        """Run a GitHub GraphQL query and return the issue/PR data from it.

        Parameters
        ----------
        query : string
          The GitHub search query to run. This is similar to whatever you'd use
          to search on GitHub.com.
        display_progress : bool
          Whether to display a progress bar as data is fetched.
        auth : string | None
          An authentication token for GitHub. If None, then the environment
          variable `GITHUB_ACCESS_TOKEN` will be tried.
        """
        self.query = query
        self.bot_users = set()  # Store detected bot usernames

        # Authentication
        token = auth or os.environ.get("GITHUB_ACCESS_TOKEN")
        if not token:
            raise ValueError(
                "Either the environment variable GITHUB_ACCESS_TOKEN or the "
                "--auth flag or must be used to pass a Personal Access Token "
                "needed by the GitHub API. You can generate a token at "
                "https://github.com/settings/tokens/new. Note that while "
                "working with a public repository, you don't need to set any "
                "scopes on the token you create."
            )
        self.auth = TokenAuth(token)

        self.gql_template = gql_template
        self.display_progress = display_progress

    def request(self, n_pages=100, n_per_page=50):
        """Make a request to the GitHub GraphQL API.

        This generates an attribute `self.data` with a pandas
        DataFrame of the issue / PR activity corresponding to
        the query you ran.
        """

        # NOTE: This main search query has a type, but the query string also has a type.
        # ref ("search"): https://developer.github.com/v4/query/#connections
        # Collect paginated issues
        pageInfo = None
        self.issues_and_or_prs = []
        for ii in range(n_pages):
            github_search_query = [
                "first: %s" % n_per_page,
                'query: "%s"' % self.query,
                "type: ISSUE",
            ]
            if ii != 0:
                github_search_query.append('after: "%s"' % pageInfo["endCursor"])

            ii_gql_query = self.gql_template.format(
                query=", ".join(github_search_query),
                comments=comments_query,
                base_elements=base_elements,
                reviews=reviews_query,
                commits=commits_query,
            )
            ii_request = requests.post(
                "https://api.github.com/graphql",
                json={"query": ii_gql_query},
                auth=self.auth,
            )
            if ii_request.status_code != 200:
                raise Exception(
                    "Query failed to run by returning code of {}. {}".format(
                        ii_request.status_code, ii_gql_query
                    )
                )
            if "errors" in ii_request.json().keys():
                raise Exception(
                    "Query failed to run with error {}. {}".format(
                        ii_request.json()["errors"], ii_gql_query
                    )
                )
            self.last_request = ii_request

            # Parse the response for this pagination
            json = ii_request.json()["data"]["search"]
            if ii == 0:
                if json["issueCount"] == 0:
                    print("Found no entries for query.", file=sys.stderr)
                    self.data = pd.DataFrame()
                    return

                n_pages = int(np.ceil(json["issueCount"] / n_per_page))
                print(
                    "Found {} items, which will take {} pages".format(
                        json["issueCount"], n_pages
                    ),
                    file=sys.stderr,
                )
                prog = tqdm(
                    total=json["issueCount"],
                    desc="Downloading:",
                    unit="issues",
                    disable=n_pages == 1 or not self.display_progress,
                )

            # Add the JSON to the raw data list
            self.issues_and_or_prs.extend(json["nodes"])
            pageInfo = json["pageInfo"]
            self.last_query = ii_gql_query

            # Update progress and should we stop?
            prog.update(len(json["nodes"]))
            if not pageInfo["hasNextPage"]:
                break

        # Extract bot users from raw data before DataFrame conversion
        def is_bot(user_dict):
            """Check if a GraphQL user object represents a bot account."""
            return user_dict and user_dict.get("__typename") == "Bot"

        bot_users = set()
        for item in self.issues_and_or_prs:
            # Check author
            author = item.get("author")
            if is_bot(author):
                bot_users.add(author["login"])

            # Check mergedBy
            merged_by = item.get("mergedBy")
            if is_bot(merged_by):
                bot_users.add(merged_by["login"])

            # Check reviewers
            reviews = item.get("reviews")
            if reviews:
                for review in reviews.get("edges", []):
                    review_author = review["node"].get("author")
                    if is_bot(review_author):
                        bot_users.add(review_author["login"])

            # Check commenters
            comments = item.get("comments")
            if comments:
                for comment in comments.get("edges", []):
                    comment_author = comment["node"].get("author")
                    if is_bot(comment_author):
                        bot_users.add(comment_author["login"])

            # Check commit authors and committers
            commits = item.get("commits")
            if commits:
                for commit_edge in commits.get("edges", []):
                    commit = commit_edge["node"]["commit"]
                    # Check committer
                    committer = commit.get("committer")
                    if committer and committer.get("user"):
                        if is_bot(committer["user"]):
                            bot_users.add(committer["user"]["login"])
                    # Check authors
                    authors = commit.get("authors")
                    if authors:
                        for author_edge in authors.get("edges", []):
                            author_user = author_edge["node"].get("user")
                            if author_user and is_bot(author_user):
                                bot_users.add(author_user["login"])

        # Create a dataframe of the issues and/or PRs
        self.data = pd.DataFrame(self.issues_and_or_prs)
        self.data.attrs["bot_users"] = bot_users

        # Add some extra fields
        def get_login(user):
            return user["login"] if not pd.isna(user) else user

        self.data["author"] = self.data["author"].map(get_login)
        self.data["mergedBy"] = self.data["mergedBy"].map(get_login)

        self.data["org"] = self.data["url"].map(lambda a: a.split("/")[3])
        self.data["repo"] = self.data["url"].map(lambda a: a.split("/")[4])
        self.data["labels"] = self.data["labels"].map(
            lambda a: [edge["node"]["name"] for edge in a["edges"]]
        )
        self.data["kind"] = self.data["url"].map(
            lambda a: "issue" if "issues/" in a else "pr"
        )

        self.data["thumbsup"] = self.data["reactions"].map(lambda a: a["totalCount"])
        self.data.drop(columns="reactions", inplace=True)

        def get_reviewers(reviews):
            """map review graph to unique list of reviewers"""
            if pd.isna(reviews) or not reviews:
                return []
            return sorted(
                set([review["node"]["author"]["login"] for review in reviews["edges"]])
            )

        self.data["reviewers"] = self.data["reviews"].map(get_reviewers)

        def get_committers(commits):
            """map commit graph to non-unique ordered list of commit authors"""
            if pd.isna(commits) or not commits:
                return []
            committers = []
            for commit in commits["edges"]:
                commit = commit["node"]["commit"]
                commit_authors = []
                for author in commit["authors"]["edges"]:
                    author = author["node"]
                    if author and author["user"]:
                        commit_authors.append(author["user"]["login"])
                    committer = commit["committer"]
                    if (
                        committer
                        and committer["user"]
                        and committer["user"]["login"] not in commit_authors
                    ):
                        commit_authors.append(committer["user"]["login"])
                committers.extend(commit_authors)
            return committers

        self.data["committers"] = self.data["commits"].map(get_committers)
