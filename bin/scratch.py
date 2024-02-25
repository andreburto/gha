from sh import git

__author__ = "Andrew Burton"


def main() -> None:
    git.fetch("--all")
    git.checkout("master")
    git.checkout("-b", "feature/test")
    git.commit("-am", "Test Commit")
    git.push()


if __name__ == "__main__":
    main()
