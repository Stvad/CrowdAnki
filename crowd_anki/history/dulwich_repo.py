import logging

from dataclasses import dataclass, field
from dulwich import porcelain
from dulwich.repo import Repo
from pathlib import Path

from .anki_repo import AnkiRepo

logger = logging.getLogger(__name__)


@dataclass
class DulwichAnkiRepo(AnkiRepo):
    repo_path: Path
    dulwich_repo: Repo = field(init=False)

    def init(self):
        path_string = str(self.repo_path.resolve())
        try:
            self.dulwich_repo = porcelain.init(path_string)
        except FileExistsError:
            logger.info(f"Using existing repository at the following path: {self.repo_path}")
            self.dulwich_repo = Repo(path_string)

    def stage_all(self):
        status = self.status()
        self.dulwich_repo.stage(status.untracked + status.unstaged)

    def commit(self, message: str = None):
        porcelain.commit(self.dulwich_repo, message=message or str(self.status()))

    def status(self):
        return porcelain.status(self.dulwich_repo)
