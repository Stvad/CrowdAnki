import logging

from dataclasses import dataclass, field
from dulwich import porcelain
from dulwich.porcelain import GitStatus
from dulwich.repo import Repo
from itertools import chain
from pathlib import Path
from typing import Any

from .anki_repo import AnkiRepo

logger = logging.getLogger(__name__)


@dataclass
class DulwichAnkiRepo(AnkiRepo):
    repo_path: Path
    git: Any = porcelain
    dulwich_repo: Repo = field(init=False)

    def __post_init__(self):
        path_string = str(self.repo_path.resolve())
        try:
            self.dulwich_repo = self.git.init(path_string)
        except FileExistsError:
            logger.info(f"Using existing repository at the following path: {self.repo_path}")
            self.dulwich_repo = Repo(path_string)

    def stage_all(self):
        status = self.status()
        self.dulwich_repo.stage(status.untracked + status.unstaged)

    def commit(self, message: str = None):
        if self.there_are_staged_changes():
            self.git.commit(self.dulwich_repo, message=message or str(self.status()))

    def there_are_staged_changes(self):
        return bool(list(chain(*self.status().staged.values())))

    def status(self) -> GitStatus:
        return self.git.status(self.dulwich_repo)

    def close(self):
        self.dulwich_repo.close()
