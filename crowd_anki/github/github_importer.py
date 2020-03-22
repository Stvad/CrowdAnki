import tempfile
import zipfile
from urllib.error import HTTPError, URLError
from urllib.request import urlopen
import sys
from io import BytesIO
from pathlib import Path

import aqt.utils
from aqt import QInputDialog
from ..importer.anki_importer import AnkiJsonImporter
from ..utils import utils
from ..git.repo import Repo
from ..git.exc import GitCommandNotFound, InvalidGitRepositoryError

BRANCH_NAME = "master"
GITHUB_ZIP_URL = "https://github.com/{}/archive/" + BRANCH_NAME + ".zip"
GITHUB_REPO_URL = "https://github.com/{}.git"


class GithubImporter(object):
    """
    Provides functionality of installing shared deck from GitHub, by entering User and Repository names
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

    def download_and_import(self, github_repo):
        try:
            try:
                self.download_and_import_git(github_repo)
            except GitCommandNotFound:  # Git not available. Use .zip archive instead
                print('Error accessing the git executable.\n '
                      'Please make sure git is installed and available on your PATH.\n'
                      'Downgrading to zip archive download.')
                self.download_and_import_zip(github_repo)

        except Exception as error:
            # aqt.utils.showWarning("Error while trying to get deck from Github: {}".format(error))
            raise error

    def download_and_import_git(self, github_repo):
        repo = None
        repo_parts = github_repo.split("/")
        repo_dir = Path(self.collection.media.dir()).joinpath("..", "CrowdAnkiGit", repo_parts[0], repo_parts[1])
        try:
            repo_dir.mkdir(parents=True, exist_ok=True)
            repo = Repo(repo_dir)
            repo.remote("origin").pull()
        except InvalidGitRepositoryError:  # Clone repository
            Repo.clone_from(GITHUB_REPO_URL.format(github_repo), repo_dir)

        AnkiJsonImporter.import_deck_from_path(self.collection, repo_dir)

    def download_and_import_zip(self, repo):
        try:
            response = urlopen(GITHUB_ZIP_URL.format(repo))
            response_sio = BytesIO(response.read())
            with zipfile.ZipFile(response_sio) as repo_zip:
                repo_zip.extractall(tempfile.tempdir)

            deck_base_name = repo.split("/")[-1]
            deck_directory_wb = Path(tempfile.tempdir).joinpath(deck_base_name + "-" + BRANCH_NAME)
            deck_directory = Path(tempfile.tempdir).joinpath(deck_base_name)
            utils.fs_remove(deck_directory)
            deck_directory_wb.rename(deck_directory)
            # Todo progressbar on download

            AnkiJsonImporter.import_deck_from_path(self.collection, deck_directory)

        except (URLError, HTTPError, OSError) as error:
            aqt.utils.showWarning("Error while trying to get deck from GitHub: {}".format(error))
            raise