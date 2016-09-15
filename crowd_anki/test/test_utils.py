import unittest
from crowd_anki.thirdparty.pathlib import Path
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