from pathlib import Path

def is_dir_exists(path):
    return Path(path).is_dir()