import os

def get_path():
    return os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))