import os

def create_dir(fpath: str) -> None:
    if not os.path.exists(fpath):
        os.makedirs(fpath)