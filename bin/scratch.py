import github
import os
import sys

from sh import git

__author__ = "Andrew Burton"

MERGE_INDICATOR = "Merge pull request"
GITHUB_API_TOKEN = os.getenv("GH_API_KEY")


def main() -> None:
    last_merge_log_line = git.log("--no-color", "--oneline", "-n", "1")

    if not MERGE_INDICATOR in last_merge_log_line:
        print("Last commit was not the merge, exiting")
        sys.exit(0)

    pr_number = last_merge_log_line.split(MERGE_INDICATOR)[1].split(" ")[1].replace("#", "")
    print(f"PR Number: {pr_number}")

    auth_token = github.Auth.Token(GITHUB_API_TOKEN)
    github_object = github.Github(auth=auth_token)
    repo = github_object.get_repo("andreburto/gha")
    pr = repo.get_pull(int(pr_number))

    print(f"Target branch: {pr.base.ref}")
    print(f"Source branch: {pr.head.ref}")



if __name__ == "__main__":
    main()
