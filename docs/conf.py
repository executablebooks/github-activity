# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
# -- Path setup --------------------------------------------------------------
# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))
# -- Project information -----------------------------------------------------

project = "GitHub Activity"
copyright = "2023, Executable Books"
author = "Executable Books Team"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ["myst_parser"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_book_theme"
html_theme_options = {
    "logo": {
        "text": "github-activity",
    },
    "icon_links": [
        {
            "url": "https://github.com/executablebooks/github-activity",
            "icon": "fa-brands fa-github",
        }
    ],
}

# Add a table of the supported PR types, tags, etc
from github_activity.github_activity import TAGS_METADATA_BASE

table_content = []
for key, vals in TAGS_METADATA_BASE.items():
    cont = [
        key,
        " ".join(vals["tags"]),
        " ".join(vals["pre"]),
        f'"{vals["description"]}"',
    ]
    table_content.append(", ".join(cont))

table_content = "\n".join(table_content)
table_template = f"""
```{{csv-table}} List of PR types
:header: PR type, Tags, Prefix, Description

{table_content}
```
"""

from pathlib import Path

path_tmp = Path(__file__).parent / "_build/dirhtml"
path_tmp.mkdir(exist_ok=True, parents=True)
path_tagslist = path_tmp / "tags_list.txt"
path_tagslist.write_text(table_template)
