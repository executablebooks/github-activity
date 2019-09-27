from setuptools import setup, find_packages
import os
import os.path as op
from glob import glob
from github_activity import __version__

# Source dependencies from requirements.txt file.
with open('requirements.txt', 'r') as f:
    lines = f.readlines()
    install_packages = [line.strip() for line in lines]

setup(
    name='github_activity',
    version=__version__,
    install_requires=install_packages,
    include_package_data=True,
    python_requires='>=3.4',
    author='Chris Holdgraf',
    author_email='choldgraf@berkeley.edu',
    url='https://jupyter.org/',
    # this should be a whitespace separated string of keywords, not a list
    keywords="development changelog",
    description="Grab recent issue/PR activity from a GitHub repository and render it as markdown.",
    long_description=open('./README.md', 'r').read(),
    long_description_content_type='text/markdown',
    license='BSD',
    packages=find_packages(),
    use_package_data=True,
    entry_points={
        'console_scripts': [
            'github-activity = github_activity.cli:main',
        ]
    },
)
