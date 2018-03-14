import urllib.request, urllib.error, urllib.parse
import zipfile
import tempfile
import io

from crowd_anki.utils import utils
from crowd_anki.thirdparty.pathlib import Path
from crowd_anki.anki_importer import AnkiJsonImporter

import aqt.utils

from aqt import QInputDialog

BRANCH_NAME = "master"
GITHUB_LINK = "https://github.com/{}/archive/" + BRANCH_NAME + ".zip"


class GithubImporter(object):
    """
    Provides functionality of installing shared deck from Github, by entering User and Repository names
    """

    def __init__(self, collection):
        self.collection = collection

    @staticmethod
    def on_github_import_action(collection):
        github_importer = GithubImporter(collection)
        github_importer.import_from_github()

    def import_from_github(self):
        repo, ok = QInputDialog.getText(None, 'Enter GitHub repository',
                                        'Path:', text='<name>/<repository>')
        if repo and ok:
            self.download_and_import(repo)

    def download_and_import(self, repo):
        try:
            response = urllib.request.urlopen(GITHUB_LINK.format(repo))
            response_sio = io.StringIO(response.read())
            with zipfile.ZipFile(response_sio) as repo_zip:
                repo_zip.extractall(tempfile.tempdir)

            deck_base_name = repo.split("/")[-1]
            deck_directory_wb = Path(tempfile.tempdir).joinpath(deck_base_name + "-" + BRANCH_NAME)
            deck_directory = Path(tempfile.tempdir).joinpath(deck_base_name)
            utils.fs_remove(deck_directory)
            deck_directory_wb.rename(deck_directory)
            # Todo progressbar on download

            AnkiJsonImporter.import_deck(self.collection, deck_directory)

        except (urllib.error.URLError, urllib.error.HTTPError, OSError) as error:
            aqt.utils.showWarning("Error while trying to get deck from Github: {}".format(error))
            raise
