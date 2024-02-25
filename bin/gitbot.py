import argparse
import os
import sys

from github import Auth, Github
from sh import git

__author__ = "Andrew Burton"

# Global Variables
GITHUB_API_TOKEN_KEY = "GH_API_KEY"


def setup_args() -> argparse.ArgumentParser:
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


def main() -> None:
    args = setup_args()

    print(dir(args))

    auth = Auth.Token(args.api_key)

    # Public Web Github
    g = Github(auth=auth)

    repo = g.get_repo(args.repo)
    branch = repo.get_branch(args.branch)

    print(dir(branch))

    g.close()

    if "feature" in args.branch:
        print("This is a feature branch")
        sys.exit()

    git.fetch("--all")
    git.checkout("master")
    git.checkout("-b", "feature/test")
    git.merge(args.branch)
    git.commit("-am", "Test Commit")
    git.push()


if __name__ == "__main__":
    main()
