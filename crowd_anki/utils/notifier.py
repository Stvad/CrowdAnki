from abc import ABC, abstractmethod

import aqt.utils
import aqt


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

def run_closure_in_main(closure):
    """Run the closure in the main thread.

This is necessary, because GUI operations in a background thread cause
a crash.  For instance, export is now run in a background thread.

    """
    if aqt.mw.inMainThread():
        closure()
    else:
        aqt.mw.taskman.run_on_main(lambda: aqt.mw.progress.timer(0, closure, False))

class AnkiModalNotifier(Notifier):
    def info(self, title: str, message: str):
        run_closure_in_main(lambda: aqt.utils.showInfo(message, title=title))

    def warning(self, title: str, message: str):
        run_closure_in_main(lambda: aqt.utils.showWarning(message, title=title))

    def error(self, title: str, message: str):
        run_closure_in_main(lambda: aqt.utils.showCritical(message, title=title))


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
