from abc import ABC, abstractmethod


class FileProvider(ABC):
    @abstractmethod
    def get_files(self, ) -> set:
        pass
