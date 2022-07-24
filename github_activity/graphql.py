import os
import sys

import numpy as np
import pandas as pd
import requests
from tqdm.auto import tqdm

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
        body
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
        }}
        mergeCommit {{
          oid
        }}
        baseRefName
        {comments}
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

        # Authentication
        auth = auth or os.environ.get("GITHUB_ACCESS_TOKEN")
        if not auth:
            raise ValueError(
                "Either the environment variable GITHUB_ACCESS_TOKEN or the "
                "--auth flag or must be used to pass a Personal Access Token "
                "needed by the GitHub API. You can generate a token at "
                "https://github.com/settings/tokens/new. Note that while "
                "working with a public repository, you don’t need to set any "
                "scopes on the token you create."
            )
        self.headers = {"Authorization": "Bearer %s" % auth}

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
            )
            ii_request = requests.post(
                "https://api.github.com/graphql",
                json={"query": ii_gql_query},
                headers=self.headers,
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

        # Create a dataframe of the issues and/or PRs
        self.data = pd.DataFrame(self.issues_and_or_prs)

        # Add some extra fields
        self.data["author"] = self.data["author"].map(
            lambda a: a["login"] if a is not None else a
        )
        self.data["org"] = self.data["url"].map(lambda a: a.split("/")[3])
        self.data["repo"] = self.data["url"].map(lambda a: a.split("/")[4])
        self.data["thumbsup"] = self.data["reactions"].map(lambda a: a["totalCount"])
        self.data.drop(columns="reactions", inplace=True)
