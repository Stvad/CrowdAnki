from pathlib import Path
import sys
from aqt import QInputDialog

from dulwich import porcelain
from dulwich.errors import NotGitRepository
from ..importer.anki_importer import AnkiJsonImporter

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
            self.download_and_import_git(repo)

    def download_and_import_git(self, github_repo):
        repo_parts = github_repo.split("/")
        repo_dir = Path(self.collection.media.dir()).joinpath("..", "CrowdAnkiGit", repo_parts[0], repo_parts[1])
        try:
            repo_dir.mkdir(parents=True, exist_ok=True)
            porcelain.pull(porcelain.open_repo(str(repo_dir)), GITHUB_REPO_URL.format(github_repo))
        except NotGitRepository:  # Clone repository
            porcelain.clone(GITHUB_REPO_URL.format(github_repo), repo_dir, False, True, porcelain.NoneStream(), porcelain.NoneStream())

        AnkiJsonImporter.import_deck_from_path(self.collection, repo_dir)
