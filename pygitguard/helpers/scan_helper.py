import os
import re
from logging import Logger

import yaml

from pygitguard.config.pygitguard_constants import (
    BEST_PRACTICES_FILES,
    INTERNAL_FILE_IGNORE,
    MAX_FILE_SIZE_MB,
    PYGITGUARD_FILENAME,
    SENSITIVE_CONTENT,
    SENSITIVE_PATTERNS,
)
from pygitguard.helpers.git_helper import is_ignored_by_gitignore


class PyGitGuardScan:
    """
    A class to scan a Git repository for potential security and best practice issues.

    This class performs several checks on the repository including:
    - Presence of best practice files as defined in configuration constants.
    - Detection of sensitive filenames using regex patterns.
    - Identification of files exceeding a maximum size limit.
    - Searching for sensitive content patterns inside files.

    It supports configuration overrides through a `gitguard.yaml` file in the repository root.

    Attributes
    ----------
    logger : logging.Logger
        Logger instance used to output informational, warning, and critical messages during scanning.
    block_commit : bool
        Flag indicating whether the commit should be blocked due to detected anomalies.

    Methods
    -------
    scan_repository(base_path)
        Scans the repository at the given path, updating `block_commit` if any issues are found.
    """

    def __init__(self, logger: Logger):
        """
        Initializes the PyGitGuardScan instance with a logger.

        Parameters
        ----------
        logger : Logger
            An instance of a logging.Logger to be used for logging messages
            during the scan process.

        Attributes
        ----------
        block_commit : bool
            A flag indicating whether the commit should be blocked due
            to detected issues. Initialized to False.
        """

        self.logger = logger
        self.block_commit = False  # <- flag de bloqueio de commit

    def __get_value_case_insensitive(self, d: dict, key: str):
        """
        Retrieves a value from the given dictionary, ignoring key case.

        Args:
        - d (dict): The dictionary to search in.
        - key (str): The key to find.

        Returns:
        - The value associated with the given key.

        Raises:
        - KeyError: If the key is not found.
        """
        key_lower = key.lower()
        for k, v in d.items():
            if k.lower() == key_lower:
                return v
        raise KeyError(f"Key '{key}' not found")

    def load_pygitguard_config(self, base_path):
        """
        Loads configuration from the project root's `gitguard.yaml` file.

        If the file does not exist, the default configuration is returned.

        Parameters
        ----------
        base_path : str
            The path to the project root.

        Returns
        -------
        tuple
            A tuple containing the maximum file size in megabytes,
            sensitive content regex patterns, and sensitive file patterns.
        """
        config_path = os.path.join(base_path, PYGITGUARD_FILENAME)
        if not os.path.isfile(config_path):
            return (
                MAX_FILE_SIZE_MB,
                SENSITIVE_CONTENT,
                SENSITIVE_PATTERNS,
                INTERNAL_FILE_IGNORE,
                BEST_PRACTICES_FILES,
            )

        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}

        return (
            config.get("MAX_FILE_SIZE_MB", MAX_FILE_SIZE_MB),
            config.get("SENSITIVE_CONTENT", SENSITIVE_CONTENT),
            config.get("SENSITIVE_PATTERNS", SENSITIVE_PATTERNS),
            config.get("INTERNAL_FILE_IGNORE", INTERNAL_FILE_IGNORE),
            config.get("BEST_PRACTICES_FILES", BEST_PRACTICES_FILES),
        )

    def check_best_practices(self, base_path, best_practices_files):
        """
        Verifies if the best practices files are present in the repository.

        Files in `BEST_PRACTICES_FILES` are checked against the files in the
        repository root. If a file is not found, a recommendation message is
        logged and the commit is blocked.

        Args:
            base_path: The path to the repository root.

        Returns:
            None
        """
        files_in_dir = [f.lower() for f in os.listdir(base_path)]

        for item in best_practices_files:
            if isinstance(item, dict):
                src = list(item.keys())[0].lower()
                target = self.__get_value_case_insensitive(item, src)
                if src in files_in_dir and target.lower() not in files_in_dir:
                    self.logger.info(
                        f"RECOMENDED: you are using '{src}' → consider adding best practice file '{target}'"
                    )
                    self.block_commit = True
            else:
                if item.lower() not in files_in_dir:
                    self.logger.info(f"RECOMENDED: create best practice file '{item}'")
                    self.block_commit = True

    def check_sensitive_filenames(
        self, filename, rel_path, patterns, internal_file_ignore
    ):
        """
        Checks if a file's name matches any of the given patterns.

        If a file's name matches any of the given patterns, a warning is logged
        and the commit is blocked.

        Parameters
        ----------
        filename : str
            The name of the file being checked.
        rel_path : str
            The relative path to the file from the base path.
        patterns : list[str]
            A list of regex patterns to search for within the file's name.

        Returns
        -------
        None
        """
        for pattern in patterns:
            if (
                re.search(pattern, filename, re.IGNORECASE)
                and filename not in internal_file_ignore
            ):
                self.logger.warning(f"POSSIBLY: sensitive file name: '{rel_path}'")
                self.block_commit = True  # ← bloqueia commit

    def check_large_file(self, full_path, rel_path, max_size_mb, internal_file_ignore):
        """
        Checks if a file exceeds the maximum allowed size and logs a warning if it does.

        Parameters
        ----------
        full_path : str
            The absolute path to the file being checked.
        rel_path : str
            The relative path of the file from the base path.
        max_size_mb : int
            The maximum file size in megabytes allowed before triggering a warning.

        Notes
        -----
        If the file size exceeds the specified limit, a warning is logged and the
        commit block flag is set to True.
        """

        if (
            os.path.getsize(full_path) > max_size_mb * 1024 * 1024
            and full_path not in internal_file_ignore
        ):

            self.logger.critical(f"LARGE FILE: {rel_path}")
            self.block_commit = True  # ← bloqueia commit

    def check_sensitive_content(self, full_path, rel_path, patterns):
        """
        Checks a file for sensitive content based on provided regex patterns.

        Parameters
        ----------
        full_path : str
            The full path to the file being checked.
        rel_path : str
            The relative path to the file being checked, used for logging.
        patterns : list of str
            A list of regex patterns to search for within the file's content.

        If sensitive content matching any of the patterns is found, a critical log
        message is recorded and the commit is blocked by setting `self.block_commit`
        to True.
        """

        if os.path.basename(full_path) in INTERNAL_FILE_IGNORE:
            return

        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
            for idx, line in enumerate(f, 1):
                for pattern in patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        self.logger.critical(
                            f"SENSITIVE content in: {rel_path} line:{idx}: {line.strip()}"
                        )
                        self.block_commit = True  # ← bloqueia commit

    def scan_repository(self, base_path):
        """
        Scans the given repository for sensitive content, large files, and best practices.

        Parameters
        ----------
        base_path : str
            The path to the root of the repository

        Returns
        -------
        bool
            True if any issues were detected, False if the repository is clean
        """
        (
            max_size_mb,
            sensitive_content,
            sensitive_patterns,
            internal_file_ignore,
            best_pratices_files,
        ) = self.load_pygitguard_config(base_path)
        self.check_best_practices(base_path, best_pratices_files)

        for root, _, files in os.walk(base_path):
            for filename in files:
                full_path = os.path.join(root, filename)
                rel_path = os.path.relpath(full_path, base_path)

                if is_ignored_by_gitignore(full_path, base_path):
                    continue

                self.check_sensitive_filenames(
                    filename,
                    rel_path,
                    sensitive_patterns,
                    internal_file_ignore,
                )
                self.check_large_file(
                    full_path, rel_path, max_size_mb, internal_file_ignore
                )
                self.check_sensitive_content(full_path, rel_path, sensitive_content)

        return self.block_commit
