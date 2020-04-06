from pathlib import Path
from aqt import QInputDialog

from dulwich import porcelain
from dulwich.errors import NotGitRepository, GitProtocolError
from ..importer.anki_importer import AnkiJsonImporter

BRANCH_NAME = "master"

class GitImporter(object):
    """
    Provides functionality of cloning a git repository that contains CrowdAnki export data, and importing it into Anki
    """

    def __init__(self, collection):
        self.collection = collection

    @staticmethod
    def on_git_import_action(collection):
        GitImporter(collection).import_from_git()

    def import_from_git(self):
        repo, ok = QInputDialog.getText(None, 'Import git repository',
                                        'URL:', text='')
        if repo and ok:
            self.clone_repository_and_import(repo)

    def clone_repository_and_import(self, repo_url):
        repo_parts = repo_url.split("/")
        repo_dir = Path(self.collection.media.dir()).joinpath("..", "CrowdAnkiGit", repo_parts[-1].split(".")[0])
        repo_dir_str = str(repo_dir)
        try:
            porcelain.pull(porcelain.open_repo(repo_dir_str, repo_url))
        except NotGitRepository:  # Clone repository
            try:
                repo_dir.mkdir(parents=True, exist_ok=True)
                porcelain.clone(repo_url, target=repo_dir_str, bare=False, checkout=True, errstream=porcelain.NoneStream(),
                    outstream=porcelain.NoneStream())
            except GitProtocolError as error: # git repository not found at that URL; but not sure how to display a more user-friendly error message
                raise error

        AnkiJsonImporter.import_deck_from_path(self.collection, repo_dir)
