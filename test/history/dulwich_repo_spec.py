from tempfile import TemporaryDirectory

from dulwich import porcelain
from expects import expect, equal, contain
from expects.matchers.built_in import not_, be_none
from mamba import description, it, context
from pathlib import Path

from crowd_anki.history.dulwich_repo import DulwichAnkiRepo


def assert_repo_exists_at_given_path_after_init(repository_path):
    repository = DulwichAnkiRepo(repository_path)

    expect(repository.dulwich_repo).to(not_(be_none))
    expect(repository.dulwich_repo.path).to(equal(str(repository_path.resolve())))


def repo_with_new_file(directory):
    repository_path = Path(directory)
    new_file = repository_path.joinpath('new_file')
    new_file.touch()

    repository = DulwichAnkiRepo(repository_path)
    repository.stage_all()

    return repository, new_file


def staged_files(repository):
    staged = porcelain.status(repository.dulwich_repo).staged
    return staged['modify'] + staged['add']


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

    with it('commits only if there are changes present'):
        pass
