from tempfile import TemporaryDirectory

from dulwich import porcelain
from dulwich.porcelain import GitStatus
from expects import expect, equal, contain
from expects.matchers.built_in import not_, be_none
from mamba import description, it, context
from pathlib import Path
from unittest.mock import MagicMock

from crowd_anki.history.dulwich_repo import DulwichAnkiRepo


def assert_repo_exists_at_given_path_after_init(repository_path):
    repository = DulwichAnkiRepo(repository_path)

    expect(repository.dulwich_repo).to(not_(be_none))
    expect(repository.dulwich_repo.path).to(equal(str(repository_path.resolve())))


def repo_with_new_file(directory, git_interface=porcelain):
    repository_path = Path(directory)
    new_file = repository_path.joinpath('new_file')
    new_file.touch()

    repository = DulwichAnkiRepo(repository_path, git_interface)
    repository.stage_all()

    return repository, new_file


def staged_files(repository):
    staged = porcelain.status(repository.dulwich_repo).staged
    return staged['modify'] + staged['add']


def mock_git_interface(add=tuple()):
    git = MagicMock()
    git.status.return_value = GitStatus(dict(add=add, modify=[], delete=[]), [], [])
    return git


with description(DulwichAnkiRepo) as self:
    with context('init'):
        with it("should use existing repo if it's present"):
            with TemporaryDirectory() as dir_name:
                repo_path = Path(dir_name)
                dulwich_repo = porcelain.init(repo_path)

                assert_repo_exists_at_given_path_after_init(repo_path)

        with it('should create a new repo if it does not exist'):
            with TemporaryDirectory() as dir_name:
                repo_path = Path(dir_name)

                assert_repo_exists_at_given_path_after_init(repo_path)

    with context('add_all'):
        with it("should add new files"):
            with TemporaryDirectory() as dir_name:
                repo, file = repo_with_new_file(dir_name)

                expect(staged_files(repo)).to(contain(str(file.name).encode()))

        with it("should add modified files"):
            with TemporaryDirectory() as dir_name:
                repo, file = repo_with_new_file(dir_name)

                repo.commit()
                file.write_text("data")
                repo.stage_all()

                expect(staged_files(repo)).to(contain(str(file.name).encode()))

    with context('commit'):
        with it('performs no commit if there are no changes'):
            with TemporaryDirectory() as dir_name:
                git_mock = mock_git_interface()

                DulwichAnkiRepo(Path(dir_name), git_mock).commit()

                git_mock.commit.assert_not_called()

        with it('performs commit when new files are added'):
            with TemporaryDirectory() as dir_name:
                git_mock = mock_git_interface(('new_file',))

                DulwichAnkiRepo(Path(dir_name), git_mock).commit()

                git_mock.commit.assert_called_once()
