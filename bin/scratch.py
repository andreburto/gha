import github
import os

import gitbot

__author__ = "Andrew Burton"

MERGE_INDICATOR = "Merge pull request"
GITHUB_API_TOKEN = os.getenv("GH_API_KEY")


def main() -> None:

    auth_token = github.Auth.Token(GITHUB_API_TOKEN)
    github_object = github.Github(auth=auth_token)
    repo = github_object.get_repo("andreburto/gha")

    pr = gitbot.get_previous_pull_request(repo)

    print(pr)


if __name__ == "__main__":
    main()
