import os

import pathspec


def is_ignored_by_gitignore(path, base_path='.'):
    """
    Checks if the given 'path' (relative to base_path) is ignored by .gitignore.
    """
    gitignore_path = os.path.join(base_path, '.gitignore')
    if not os.path.isfile(gitignore_path):
        return False
    with open(gitignore_path, 'r', encoding='utf-8') as f:
        patterns = f.read().splitlines()
    spec = pathspec.PathSpec.from_lines('gitwildmatch', patterns)
    rel_path = os.path.relpath(path, base_path)
    return spec.match_file(rel_path)


#
