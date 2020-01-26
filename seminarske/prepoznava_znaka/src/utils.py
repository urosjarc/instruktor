from pathlib import Path

def getDir(_file_, path='') -> str:
    return str(Path(_file_).resolve().parent.joinpath(path))
