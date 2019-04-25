#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup


# Get requirements
def get_requirements():
    with open("requirements.txt") as f:
        return f.read().splitlines()


# Setup
setup(
    name="topify",
    version="0.1.0",
    description="A user-friendly top-like monitoring",
    url="https://github.com/pcorbel/topify",
    packages=find_packages(),
    install_requires=get_requirements(),
    entry_points={"console_scripts": ["topify = topify.app:main"]},
)
