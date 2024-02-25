import argparse
import os
import sys

from datetime import datetime
from github import Auth, Github
from sh import git

__author__ = "Andrew Burton"

# Global Variables
GITHUB_API_TOKEN_KEY = "GH_API_KEY"


def setup_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="gitbot", description="Gitbot for Github",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--api-key", dest="api_key", type=str,
                        default=os.getenv(GITHUB_API_TOKEN_KEY),
                        help="The API key to use for working in this repo.")
    parser.add_argument("--branch", dest="branch", type=str, default=os.getenv("GITHUB_REF_NAME"),
                        help="The branch to work with")
    parser.add_argument("--repo", dest="repo", type=str, default=os.getenv("GITHUB_REPOSITORY"),
                        help="The repository to work with")
    return parser.parse_args()


def pick_target_branch(source_branch: str) -> str:
    target_by_branch = {
        "feature": "develop",
        "hotfix": "master",
        "release": "master",
        "bugfix": "develop",
        "develop": "release",
    }
    branch_key = source_branch.split("/")[0]
    target_branch = target_by_branch[branch_key]
    print(f"pick_target_branch - Source: {source_branch}, Target: {target_branch}")
    return target_branch


def feature_branch(args: argparse.Namespace, github_object: Github) -> None:
    target_branch = pick_target_branch(args.branch)
    repo = github_object.get_repo(args.repo)
    pr = repo.create_pull(title="Feature Branch",
                          body="This is a feature branch",
                          head=args.branch,
                          base=target_branch)
    return pr


def develop_branch(args: argparse.Namespace, github_object: Github) -> None:
    repo = github_object.get_repo(args.repo)
    date_time_str = datetime.now().strftime("%Y%m%d%H%M%S")
    git.checkout("-b", f"release/{date_time_str}")
    git.push("--set-upstream", "origin", f"release/{date_time_str}")


def main() -> None:
    function_by_branch = {
        "feature": feature_branch,
        "develop": develop_branch,
    }

    args = setup_args()

    print(dir(args))

    # Public Web GitHYub
    auth_token = Auth.Token(args.api_key)
    g = Github(auth=auth_token)

    try:
        source_branch = str(args.branch).split("/")[0]
        function_by_branch[source_branch](args, g)
    except KeyError:
        print(f"Branch function {source_branch} not supported.")
    except Exception as e:
        print(f"Error: {e}")

    g.close()


if __name__ == "__main__":
    main()
