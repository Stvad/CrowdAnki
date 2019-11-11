import tempfile
import zipfile
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from io import BytesIO
from pathlib import Path

import aqt.utils
from aqt import QInputDialog
from ..importer.anki_importer import AnkiJsonImporter
from ..config.config_settings import ConfigSettings
from ..utils import utils

BRANCH_NAME = "master"
GITHUB_LINK = "https://github.com/{}/archive/" + BRANCH_NAME + ".zip"


class GithubImporter(object):
    """
    Provides functionality of installing shared deck from GitHub, by entering User and Repository names
    """

    def __init__(self, collection, config: ConfigSettings):
        self.collection = collection
        self.config = config

    @staticmethod
    def on_github_import_action(collection, config: ConfigSettings):
        github_importer = GithubImporter(collection, config)
        github_importer.import_from_github()

    def import_from_github(self):
        repo, ok = QInputDialog.getText(None, 'Enter GitHub repository',
                                        'Path:', text='<name>/<repository>')
        if repo and ok:
            self.download_and_import(repo)

    def download_and_import(self, repo):
        try:
            response = urlopen(GITHUB_LINK.format(repo))
            response_sio = BytesIO(response.read())
            with zipfile.ZipFile(response_sio) as repo_zip:
                repo_zip.extractall(tempfile.tempdir)

            deck_base_name = repo.split("/")[-1]
            deck_directory_wb = Path(tempfile.tempdir).joinpath(deck_base_name + "-" + BRANCH_NAME)
            deck_directory = Path(tempfile.tempdir).joinpath(deck_base_name)
            utils.fs_remove(deck_directory)
            deck_directory_wb.rename(deck_directory)
            # Todo progressbar on download

            AnkiJsonImporter.import_deck_from_path(self.collection, self.config, deck_directory)

        except (URLError, HTTPError, OSError) as error:
            aqt.utils.showWarning("Error while trying to get deck from GitHub: {}".format(error))
            raise
