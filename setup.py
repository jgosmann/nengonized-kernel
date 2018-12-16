#!/usr/bin/env python

import imp
import os.path

try:
    from setuptools import find_packages, setup
except ImportError:
    raise ImportError(
        "'setuptools' is required, but not installed. "
        "See https://packaging.python.org/installing/")


version_mod = imp.load_source(
    'version',
    os.path.join(os.path.dirname(__file__), 'nengonized_kernel', 'version.py'))

setup(
    name="nengonized-kernel",
    version=version_mod.version_string,
    author="Jan Gosmann",
    author_email="jan@hyper-world.de",
    url='https://github.com/jgosmann/nengonized-kernel',
    license="proprietary",
    description="TODO",
    long_description="TODO",

    packages=find_packages(),
    provides=['nengonized_kernel'],

    install_requires=['graphene', 'nengo'],
    extras_require={
        'tests': ['pytest'],
    },

    entry_points={
    },

    classifiers=[
    ],
)
