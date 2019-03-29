from abc import ABC, abstractmethod


class AnkiRepo(ABC):
    @abstractmethod
    def stage_all(self):
        pass

    @abstractmethod
    def commit(self, message: str = None):
        pass
