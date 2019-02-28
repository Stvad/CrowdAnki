from abc import ABC, abstractmethod

from dataclasses import dataclass
from pathlib import Path


@dataclass
class AnkiRepo(ABC):
    repo_path: Path

    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def add_all(self):
        pass

    @abstractmethod
    def commit(self, message=None):
        pass
