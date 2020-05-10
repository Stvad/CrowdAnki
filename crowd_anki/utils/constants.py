from pathlib import Path

UUID_FIELD_NAME = 'crowdanki_uuid'
DECK_FILE_NAME = "deck"
SETTINGS_FIELD_NAME = '_settings'
DECK_FILE_EXTENSION = ".json"
MEDIA_SUBDIRECTORY_NAME = "media"

ANKI_EXPORT_EXTENSION = "directory"

USER_FILES_PATH = Path(__file__).parent.parent.joinpath('user_files')
