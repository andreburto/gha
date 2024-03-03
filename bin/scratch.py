import gitbot
import github
import logging
import os
import re
import sys

from sh import git

__author__ = "Andrew Burton"

MERGE_INDICATOR = "Merge pull request"
GITHUB_API_TOKEN = os.getenv("GH_API_KEY")

log_level = logging.DEBUG if str(os.getenv("DEBUG", "false")).lower() == "true" else logging.INFO
logger = logging.getLogger(__file__)
logger.setLevel(log_level)
logger.addHandler(logging.StreamHandler(stream=sys.stdout))


def main() -> None:

    last_merge_log_line = git.log("--oneline", "-n", "1")
    logger.info(f"Last merge log line: {last_merge_log_line}")
    logger.info(f"Last merge log line type: {type(last_merge_log_line)}")
    matches = re.findall(r"#\d+", last_merge_log_line)
    logger.info(f"Matches: {matches}")


if __name__ == "__main__":
    main()
