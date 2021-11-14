from pathlib import Path
from tempfile import TemporaryDirectory

from unittest.mock import MagicMock, patch
from mamba import describe, it, context
from expects import expect, equal

from crowd_anki.github.github_importer import GitImporter

TEST_GIT_REPO = "https://github.com/Stvad/Software_Engineering__git"
CLONE_REPETITIONS = 3

temp_dir = TemporaryDirectory()
repo_local_path = Path(temp_dir.name)

GitImporter.get_repo_local_path = lambda self, x: repo_local_path

with describe(GitImporter) as self:
    with context("user is trying to import a deck from a git repo multiple times"):
        # See #138!
        with it("should clone the git repo without crashing"):
            self.collection_mock = MagicMock()
            self.subject = GitImporter(self.collection_mock)
            with patch("crowd_anki.github.github_importer.AnkiJsonImporter") as mock_json_importer:
                for _ in range(0, CLONE_REPETITIONS):
                    self.subject.clone_repository_and_import(TEST_GIT_REPO)
                expect(mock_json_importer.import_deck_from_path.call_count).to(equal(3))

            # Note: the import itself isn't being tested (we're not,
            # yet (as of 2021-11) testing import itself in any
            # situation)!

temp_dir.cleanup()
