import unittest
from pathlib import Path

from crowd_anki.utils import utils


class FsRemoveTest(unittest.TestCase):
    def setUp(self):
        self.dirpath = Path("testdir")
        self.filepath = Path("testdir").joinpath("testfile")

        try:
            self.dirpath.mkdir()
        except:
            pass

        self.filepath.touch(exist_ok=True)

    def test_rmfile(self):
        self.assertTrue(self.filepath.exists())
        utils.fs_remove(self.filepath)
        self.assertFalse(self.filepath.exists())

    def test_rmdir(self):
        utils.fs_remove(self.dirpath)
        self.assertFalse(self.dirpath.exists())
        self.assertFalse(self.filepath.exists())

    def test_rm_nonexistant(self):
        # Should not crash :)
        nonexistant_path = Path("nonexistant_path")
        self.assertFalse(nonexistant_path.exists())
        utils.fs_remove(nonexistant_path)
