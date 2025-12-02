import os
import subprocess

from dataclasses import dataclass
from pathlib import Path

from .anki_repo import AnkiRepo


@dataclass
class CustomCommandRepo(AnkiRepo):
    repo_path: Path
    command: str

    def stage_all(self):
        pass

    def commit(self, message: str = None):
        env = os.environ.copy()
        env["CROWD_ANKI_COMMIT_MESSAGE"] = message

        try:
            retcode = subprocess.call(self.command, shell=True, env=env)
        except OSError as e:
            raise RuntimeError("Failed to execute custom snapshot command: %s" % e)

        if retcode != 0:
            raise RuntimeError("Custom snapshot command exited with "
                                "non-zero exit code: %d" % retcode)

    def close(self):
        pass
