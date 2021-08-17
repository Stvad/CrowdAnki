from aqt import QInputDialog
from dulwich import porcelain
from dulwich.errors import NotGitRepository, GitProtocolError

from ..config.config_settings import ConfigSettings
from ..importer.anki_importer import AnkiJsonImporter
from ..utils.notifier import AnkiModalNotifier

BRANCH_NAME = "master"


def get_repository_name(repository_url):
    repo_name = list(filter(None, repository_url.split("/")))[-1]  # using filter() in case it ends in "/"
    return repo_name.split(".")[0]  # in case it ends in ".git"


class GitImporter(object):
    """
    Provides functionality of cloning a git repository that contains CrowdAnki export data, and importing it into Anki
    """

    def __init__(self, collection):
        self.collection = collection
        self.notifier = AnkiModalNotifier()

    @staticmethod
    def on_git_import_action(collection):
        GitImporter(collection).import_from_git()

    def import_from_git(self):
        repo_url, ok = QInputDialog.getText(None, 'Import git repository', 'URL:', text='')
        if repo_url and ok:
            self.clone_repository_and_import(repo_url)

    def clone_repository_and_import(self, repo_url):
        repo_url = repo_url.strip()
        try:
            repo_local_path = self.get_repo_local_path(repo_url)
            porcelain.pull(str(repo_local_path), repo_url)
        except ValueError:
            return self.notifier.error("URL incorrect", f"URL could not be parsed \"{repo_url}\"")
        except NotGitRepository:
            try:
                self.clone_repository(repo_url, repo_local_path)
            except (GitProtocolError, NotGitRepository):
                return self.notifier.error("repository not found", f"git repository not found at URL {repo_url}")

        AnkiJsonImporter.import_deck_from_path(self.collection, repo_local_path)

    def clone_repository(self, repo_url, repo_path):
        repo_path.mkdir(parents=True, exist_ok=True)
        repo_object = porcelain.clone(repo_url, target=str(repo_path), bare=False, checkout=True, errstream=porcelain.NoneStream(),
                                      outstream=porcelain.NoneStream())
        repo_object.close()

    def get_repo_local_path(self, repo_url):
        repo_name = get_repository_name(repo_url)
        return ConfigSettings.get_instance().full_snapshot_path.joinpath(repo_name)
