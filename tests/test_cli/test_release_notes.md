## New features added

- ✨ NEW: Adding - chapter entries to _toc.yml [#817](https://github.com/executablebooks/jupyter-book/pull/817) ([@choldgraf](https://github.com/choldgraf))

  Here's an example of the TOC structure:

  ```yaml
  - file: intro
    numbered: true

  - chapter: Get started
    sections:
    - file: start/overview
    - file: start/build

  - chapter: Book pages and types
    sections:
    - file: content/markdown
    - file: content/notebooks

  - chapter: Reference and test pages
    sections:
    - file: test_pages/test
      sections:
        - file: test_pages/layout_elements
        - file: test_pages/equations
  ```

## Enhancements made

- 👌 IMPROVE: improving numbered sections [#826](https://github.com/executablebooks/jupyter-book/pull/826) ([@choldgraf](https://github.com/choldgraf))
- checking for toc modification time [#772](https://github.com/executablebooks/jupyter-book/pull/772) ([@choldgraf](https://github.com/choldgraf))

  This is an attempt at checking for the modification time of the table of contents file and forcing a re-build of all pages if this happens. We need to do this because otherwise people could change the toc, but Sphinx won't know to re-build some pages and these TOC changes won't be reflected.

  #### This heading will be included in release notes

  Here's a sub-heading
- first pass toc directive [#757](https://github.com/executablebooks/jupyter-book/pull/757) ([@choldgraf](https://github.com/choldgraf))

