from pathlib import Path
from aqt import QInputDialog
from ..config.config_settings import ConfigSettings
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
        repo_name = repo_url.split("/")[-1].split(".")[0]
        repo_path = Path(ConfigSettings.get_instance().snapshot_complete_dir).joinpath(repo_name)
        repo_dir = str(repo_path)
        try:
            porcelain.pull(porcelain.open_repo(repo_dir), repo_url)
        except NotGitRepository:  # Clone repository
            try:
                repo_path.mkdir(parents=True, exist_ok=True)
                porcelain.clone(repo_url, target=repo_dir, bare=False, checkout=True, errstream=porcelain.NoneStream(),
                    outstream=porcelain.NoneStream())
            except GitProtocolError as error: # git repository not found at that URL; but not sure how to display a more user-friendly error message
                raise error

        AnkiJsonImporter.import_deck_from_path(self.collection, repo_path)
