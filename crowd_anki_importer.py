try:
    from crowd_anki import main
except ModuleNotFoundError:
    from .crowd_anki import main
