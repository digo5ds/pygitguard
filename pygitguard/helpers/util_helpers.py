"""Utility functions for PyGitGuard configuration and setup."""

import os

import yaml

from pygitguard.__version__ import get_version
from pygitguard.config.logger import logger
from pygitguard.config.pygitguard_constants import (
    BEST_PRACTICES_FILES,
    INTERNAL_FILE_IGNORE,
    MAX_FILE_SIZE_MB,
    PYGITGUARD_FILENAME,
    SENSITIVE_CONTENT,
    SENSITIVE_PATTERNS,
)


def export_config_to_yaml(filepath=PYGITGUARD_FILENAME):
    """
    Export the current config constants to a YAML file.
    Adds a comment at the top explaining the purpose of the file.
    """
    if not os.path.exists(filepath):
        config = {
            "SENSITIVE_PATTERNS": SENSITIVE_PATTERNS,
            "SENSITIVE_CONTENT": SENSITIVE_CONTENT,
            "BEST_PRACTICES_FILES": BEST_PRACTICES_FILES,
            "MAX_FILE_SIZE_MB": MAX_FILE_SIZE_MB,
            "INTERNAL_FILE_IGNORE": INTERNAL_FILE_IGNORE,
        }
        comment = (
            "# .gitguard.yaml: Configuration file for GitGuard.\n"
            "# This file customizes sensitive file patterns, content patterns"
            ", ignored paths, and other scan settings.\n"
            "# Edit this file to adapt GitGuard's scan to your project's needs.\n"
            "# RECOMENDATION: set {project_path}/__version__.py  in BEST_PRACTICES_FILES\n\n"
        )
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(comment)
            yaml.dump(config, f, allow_unicode=True, sort_keys=False)
            logger.info(
                "The file gitguard.yaml has been created, you can configure your settings there."
            )


def create_pre_commit_config(path=".pre-commit-config.yaml"):
    """
    Creates a pre-commit configuration file for PyGitGuard.

    The configuration file enables the PyGitGuard hook, which runs the
    `pygitguard_cli` command as a pre-commit hook.

    The hook is configured to run on the current project directory, and
    its name is set to "PyGitGuard Scan".

    Parameters
    ----------
    path : str
        The path to the pre-commit configuration file to be created.
        Defaults to ".pre-commit-config.yaml".
    """
    if not os.path.exists(path):
        content = f"""
    repos:
  - repo: https://github.com/digo5ds/pygitguard
    rev:{get_version}
    hooks:
      - id: pygitguard-scan
        name: PyGitGuard Scan
        entry: pygitguard
        language: system
        types: [python]
        stages: [pre-commit]

    """
        with open(path, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
            logger.info(
                "created .pre-commit-config.yaml you can configure your hooks there."
            )
