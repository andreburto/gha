import sys

from sh import git

__author__ = "Andrew Burton"


def main() -> None:
    l = git.log("--oneline", "-n", "5", _out=sys.stdout, _err=sys.stderr)
    print(l)


if __name__ == "__main__":
    main()
