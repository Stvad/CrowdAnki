from contextlib import contextmanager

from aqt import AnkiQt


@contextmanager
def progress_indicator(window: AnkiQt, label=None):
    window.progress.start(immediate=True, label=label)
    try:
        yield
    finally:
        window.progress.finish()
