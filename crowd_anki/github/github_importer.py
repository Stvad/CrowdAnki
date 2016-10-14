import urllib2
import zipfile
import tempfile
import StringIO

from crowd_anki.utils import utils
from crowd_anki.thirdparty.pathlib import Path
from crowd_anki.anki_importer import AnkiJsonImporter
from git import Repo

import aqt.utils

from aqt import QInputDialog, QErrorMessage

BRANCH_NAME = "master"
GITHUB_LINK = "https://github.com/{}/archive/" + BRANCH_NAME + ".zip"
GITHUB_REPO = "https://github.com/{}.git"


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

    def download_and_import_git(self, github_repo, deck_base_name):
        repo = None
        try:
            repo = Repo(Path(self.collection.media.dir()).joinpath("..", "CrowdAnkiGit", deck_base_name, "git"))
            repo.remote("origin").pull()
        except git.exc.InvalidGitRepositoryError:  # New repository
            repo = Repo.clone_from(GITHUB_REPO.format(github_repo),
                                   Path(self.collection.media.dir()).joinpath("..", "CrowdAnkiGit", deck_base_name,
                                                                              "git"))
        AnkiJsonImporter.import_deck(self.collection, Path(repo.working_tree_dir))

    def download_and_import_zip(self, github_repo, deck_base_name):
        response = urllib2.urlopen(GITHUB_LINK.format(github_repo))
        response_sio = StringIO.StringIO(response.read())
        with zipfile.ZipFile(response_sio) as repo_zip:
            repo_zip.extractall(tempfile.tempdir)

        deck_directory_wb = Path(tempfile.tempdir).joinpath(deck_base_name + "-" + BRANCH_NAME)
        deck_directory = Path(tempfile.tempdir).joinpath(deck_base_name)
        utils.fs_remove(deck_directory)
        deck_directory_wb.rename(deck_directory)
        # Todo progressbar on download

        AnkiJsonImporter.import_deck(self.collection, deck_directory)

    def download_and_import(self, github_repo):
        deck_base_name = github_repo.split("/")[-1]
        try:
            try:
                self.download_and_import_git(github_repo, deck_base_name)
            except git.exc.GitCommandNotFound:  # Git not available. Use .zip archive instead
                print('Error accessing the git executable.\n '
                      'Please make sure git is installed and available on your PATH.\n'
                      'Downgrading to zip archive download.')
                self.download_and_import_zip(github_repo, deck_base_name)

        except (urllib2.URLError, urllib2.HTTPError, OSError) as error:
            aqt.utils.showWarning("Error while trying to get deck from Github: {}".format(error))
