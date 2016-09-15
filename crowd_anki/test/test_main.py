import unittest
import sys
import os

TEST_DIR = os.path.dirname(os.path.realpath(__file__))

sys.path.insert(0, "/usr/share/anki")
sys.path.insert(0, os.path.join(TEST_DIR, os.pardir, os.pardir))


if __name__ == '__main__':
    suite = unittest.TestLoader().discover(TEST_DIR)
    retcode = not unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful()
    sys.exit(retcode)