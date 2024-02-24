import argparse
import os

from github import Auth, Github


auth = Auth.Token(os.getenv("GH_API_KEY"))

# Public Web Github
g = Github(auth=auth)

repo = g.get_repo("andreburto/gha")
branch = repo.get_branch(branch="master")

print(dir(branch))

g.close()
