from setuptools import setup, find_packages
from os.path import join

PACKAGE = "fritzclient"
NAME = "fritzclient"
DESCRIPTION = "Python FritxBox interface"
AUTHOR = "Michel Albert"
AUTHOR_EMAIL = "michel@albert.lu"
with open(join(PACKAGE, 'version.txt')) as fptr:
    VERSION = fptr.read().strip()

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=open("README.rst").read(),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    include_package_data=True,
    install_requires=[
        'requests'
    ],
    packages=find_packages(exclude=["tests.*", "tests"])
)
