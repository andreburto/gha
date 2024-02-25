import argparse
import os
import sys

from github import Auth, Github
from sh import git

__author__ = "Andrew Burton"

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
