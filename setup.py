from setuptools import setup, find_packages
import os
import os.path as op
from glob import glob
from pathlib import Path

init = Path().joinpath("github_activity", "__init__.py")
for line in init.read_text().split("\n"):
    if line.startswith("__version__ ="):
        version = line.split(" = ")[-1].strip('"')
        break

# Source dependencies from requirements.txt file.
with open("requirements.txt", "r") as f:
    lines = f.readlines()
    install_packages = [line.strip() for line in lines]

setup(
    name="github_activity",
    version=version,
    include_package_data=True,
    python_requires=">=3.6",
    author="Executable Books Project",
    author_email="choldgraf@berkeley.edu",
    url="https://jupyter.org/",
    # this should be a whitespace separated string of keywords, not a list
    keywords="development changelog",
    description="Grab recent issue/PR activity from a GitHub repository and render it as markdown.",
    long_description=open("./README.md", "r").read(),
    long_description_content_type="text/markdown",
    license="BSD",
    packages=find_packages(),
    use_package_data=True,
    entry_points={"console_scripts": ["github-activity = github_activity.cli:main",]},
    install_requires=install_packages,
    extras_require={
        "testing": ["pytest", "pytest-regressions"],
        "sphinx": ["sphinx", "myst_parser", "sphinx_book_theme"],
    },
)
