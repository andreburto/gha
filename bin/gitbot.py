import argparse
import github
import logging
import os
import sys

from datetime import datetime
from sh import git

__author__ = "Andrew Burton"

# Global Variables
GITHUB_API_TOKEN_KEY = "GH_API_KEY"
MERGE_INDICATOR = "Merge pull request"
PR_BODY_TEMPLATE = """
Story: 

Description:

Source branch: {source_branch}

Target branch: {target_branch}
"""

# Set up logging
log_level = logging.DEBUG if str(os.getenv("DEBUG", "false")).lower() == "true" else logging.INFO
logger = logging.getLogger(__file__)
logger.setLevel(log_level)
logger.addHandler(logging.StreamHandler(stream=sys.stdout))


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
    logger.info(f"pick_target_branch - Source: {source_branch}, Target: {target_branch}")
    return target_branch


def get_previous_pull_request(repo: github.Repository) -> github.PullRequest:
    """
    """
    last_merge_log_line = git.log("--no-color", "--oneline", "-n", "1")

    if not MERGE_INDICATOR in last_merge_log_line:
        logger.info("Last commit was not the merge, exiting.")
        return None

    pr_number = last_merge_log_line.split(MERGE_INDICATOR)[1].split(" ")[1].replace("#", "")
    pr = repo.get_pull(int(pr_number))
    return pr


def pull_request_exists(args: argparse.Namespace, repo: github.Repository) -> bool:
    """
    """
    target_branch = pick_target_branch(args.branch)
    prs = repo.get_pulls(state="open", sort="created", base=target_branch)
    for pr in prs:
        if pr.head.ref == args.branch:
            return True
    return False


def feature_branch(args: argparse.Namespace, repo: github.Repository) -> None:
    """
    """
    if pull_request_exists(args, repo):
        logger.info(f"Pull request for {args.branch} already exists.")
        return

    target_branch = pick_target_branch(args.branch)
    repo.create_pull(
        title=args.branch,
        body=PR_BODY_TEMPLATE.format(source_branch=args.branch, target_branch=target_branch),
        head=args.branch,
        base=target_branch)


def develop_branch(args: argparse.Namespace, repo: github.Repository) -> None:
    """
    """
    pr = get_previous_pull_request(repo)

    if pr is None:
        logger.info("No previous pull request found.")
        return

    branch_prefix = pick_target_branch(args.branch)
    branch_suffix = pr.head.ref.split("/", 1)[1]
    release_branch_name = f"{branch_prefix}/{branch_suffix}"

    git.checkout("-b", release_branch_name)
    git.push("--set-upstream", "origin", release_branch_name)


def release_branch(args: argparse.Namespace, repo: github.Repository) -> None:
    """
    """
    if pull_request_exists(args, repo):
        logger.info(f"Pull request for {args.branch} already exists.")
        return

    target_branch = pick_target_branch(args.branch)
    repo.create_pull(
        title=args.branch,
        body=PR_BODY_TEMPLATE.format(source_branch=args.branch, target_branch=target_branch),
        head=args.branch,
        base=target_branch)


def master_branch(args: argparse.Namespace, repo: github.Repository) -> None:
    pass


def hotfix_branch(args: argparse.Namespace, repo: github.Repository) -> None:
    pass


def main() -> None:
    """
    """
    function_by_branch = {
        "feature": feature_branch,
        "develop": develop_branch,
        "release": release_branch,
        "master": master_branch,
        "hotfix": hotfix_branch,
    }

    args = setup_args()

    # Public Web GitHYub
    auth_token = github.Auth.Token(args.api_key)
    github_object = github.Github(auth=auth_token)
    repo = github_object.get_repo(args.repo)

    try:
        source_branch = str(args.branch).split("/")[0]
        function_by_branch[source_branch](args, repo)
    except KeyError:
        print(f"Function for {source_branch} not supported.")
    except Exception as e:
        print(f"Error: {e}")

    g.close()


if __name__ == "__main__":
    main()
