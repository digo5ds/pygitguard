#!/usr/bin/env python3
"""
GitGuard - Sensitive file scanner before commit
Author: https://github.com/digo5ds
"""

import argparse
import sys

from pygitguard.config.logger import logger
from pygitguard.helpers.scan_helper import PyGitGuardScan
from pygitguard.helpers.util_helpers import (
    create_pre_commit_config,
    export_config_to_yaml,
)


def main():
    """
    Main function to execute the GitGuard sensitive file scanner.

    This function parses command-line arguments to determine the repository path
    and whether to run in dry-run mode. It invokes the scan_repository function
    to check for security issues within the specified path. The findings are
    colorized and printed to the console. If issues are found and not in dry-run
    mode, the program exits with a status code of 1.
    """
    export_config_to_yaml()
    create_pre_commit_config()

    parser = argparse.ArgumentParser(
        description="GitGuard - Sensitive file scanner before commit"
    )
    parser.add_argument("--path", default=".", help="Repository path")
    args = parser.parse_args()

    scanner = PyGitGuardScan(logger)
    if scanner.scan_repository(args.path):
        response = input(
            "🛑 Commit blocked due to POSSIBLY sensitive issues detected. Type 'yes' to override and proceed: "
        ).lower()

        if response.lower() == "no":
            logger.warning("Commit aborted due to sensitive issues.")
            sys.exit(1)
    logger.info("Commit approved.")  # Allow the commit even with warnings
    sys.exit(0)


if __name__ == "__main__":
    main()
