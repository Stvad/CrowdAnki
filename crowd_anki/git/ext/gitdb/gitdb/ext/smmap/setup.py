#!/usr/bin/env python
import os
import codecs
try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

import smmap

if os.path.exists("README.md"):
    long_description = codecs.open('README.md', "r", "utf-8").read().replace('\r\n', '\n')
else:
    long_description = "See https://github.com/gitpython-developers/smmap"

setup(
    name="smmap",
    version=smmap.__version__,
    description="A pure Python implementation of a sliding window memory map manager",
    author=smmap.__author__,
    author_email=smmap.__contact__,
    url=smmap.__homepage__,
    platforms=["any"],
    license="BSD",
    packages=find_packages(),
    zip_safe=True,
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    classifiers=[
        # Picked from
        #    http://pypi.python.org/pypi?:action=list_classifiers
        #"Development Status :: 1 - Planning",
        #"Development Status :: 2 - Pre-Alpha",
        #"Development Status :: 3 - Alpha",
        # "Development Status :: 4 - Beta",
        "Development Status :: 5 - Production/Stable",
        #"Development Status :: 6 - Mature",
        #"Development Status :: 7 - Inactive",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    tests_require=('nose', 'nosexcover'),
    test_suite='nose.collector'
)
