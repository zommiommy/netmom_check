import os
import subprocess
from .logger import logger
from .get_path import get_path


def shell(command, cwd="", capture_stdout=False):
    """Execute shell commands and return the stdout"""
    args = {
        "args":command,
        "shell":True,
        "cwd":os.path.join(get_path(), cwd) 
    }
    logger.info("Executing %s"%args)
    if capture_stdout:
        return subprocess.check_output(**args).decode()
    else:
        return subprocess.call(**args)