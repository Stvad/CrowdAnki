from abc import ABC, abstractmethod

import aqt.utils


class Notifier(ABC):
    @abstractmethod
    def info(self, title: str, message: str):
        pass

    @abstractmethod
    def warning(self, title: str, message: str):
        pass

    @abstractmethod
    def error(self, title: str, message: str):
        pass


class AnkiUiNotifier(Notifier):
    def info(self, title: str, message: str):
        aqt.utils.showInfo(message, title=title)

    def warning(self, title: str, message: str):
        aqt.utils.showWarning(message, title=title)

    def error(self, title: str, message: str):
        aqt.utils.showCritical(message, title=title)
