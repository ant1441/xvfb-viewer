#!/usr/bin/env python
from os.path import join
from setuptools import setup

for line in open(join('xvfb_viewer', '__init__.py')):
    if '__version__' in line:
        version = eval(line.split('=')[-1])
        break
else:
    raise AssertionError('__version__ = "VERSION" must be in __init__.py')

setup(
    name="Xvfb Viewer",
    version=version,
    description="A web front end to periodically view an Xvfb screen",
    author="Adam Hodgen",
    author_email="adam.hodgen@thetestpeople.com",
    packages=["xvfb_viewer, xvfb_viewer.views"],
    install_requires=['Flask', 'numpy', 'Pillow'],
    entry_points=dict(console_scripts=['run_xvfb_view=xvfb_viewer:run']),
    include_package_data=True,
)
