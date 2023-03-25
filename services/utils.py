import os


def check_if_file_existis(path: str):
    if not os.path.isfile(path):
        raise FileNotFoundError(path)
