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


class AnkiModalNotifier(Notifier):
    def info(self, title: str, message: str):
        aqt.utils.showInfo(message, title=title)

    def warning(self, title: str, message: str):
        aqt.utils.showWarning(message, title=title)

    def error(self, title: str, message: str):
        aqt.utils.showCritical(message, title=title)


class AnkiTooltipNotifier(Notifier):
    @staticmethod
    def show_message(title: str, message: str, prefix=""):
        aqt.utils.tooltip(f"{prefix} {title}\n{message}", period=5000)

    def info(self, title: str, message: str):
        self.show_message(title, message)

    def warning(self, title: str, message: str):
        self.show_message(title, message, "Warning:")

    def error(self, title: str, message: str):
        self.show_message(title, message, "Error:")
