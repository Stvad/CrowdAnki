from contextlib import contextmanager


@contextmanager
def progress_indicator(window, label=None):
    window.progress.start(immediate=True, label=label)
    try:
        yield
    finally:
        window.progress.finish()
