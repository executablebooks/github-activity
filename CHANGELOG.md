# Changelog

## v1.1.0 - 2025-12-09

([full changelog](https://github.com/executablebooks/github-activity/compare/v1.0.3...3ffc68f920474d500c7150bde975e86c591a3184))

### Enhancements made

- Allow excluding certain usernames from changelog [#128](https://github.com/executablebooks/github-activity/pull/128) ([@stefanv](https://github.com/stefanv), [@bsipocz](https://github.com/bsipocz), [@choldgraf](https://github.com/choldgraf), [@nabobalis](https://github.com/nabobalis))
- Use GraphQL API for bot detection [#146](https://github.com/executablebooks/github-activity/pull/146) ([@choldgraf](https://github.com/choldgraf), [@stefanv](https://github.com/stefanv))
- Use latest github release first instead of github tag [#125](https://github.com/executablebooks/github-activity/pull/125) ([@choldgraf](https://github.com/choldgraf), [@nabobalis](https://github.com/nabobalis))

### Bugs fixed

- Add `pytz` to requirements [#147](https://github.com/executablebooks/github-activity/pull/147) ([@jtpio](https://github.com/jtpio), [@bsipocz](https://github.com/bsipocz), [@nabobalis](https://github.com/nabobalis))
- Ensure PRs only show up once per changelog [#130](https://github.com/executablebooks/github-activity/pull/130) ([@choldgraf](https://github.com/choldgraf), [@bsipocz](https://github.com/bsipocz), [@nabobalis](https://github.com/nabobalis))

### Maintenance and upkeep improvements

- MAINT: group the dependabot updates into one PR [#141](https://github.com/executablebooks/github-activity/pull/141) ([@bsipocz](https://github.com/bsipocz))
- Expose GitHub API call error [#138](https://github.com/executablebooks/github-activity/pull/138) ([@stefanv](https://github.com/stefanv), [@choldgraf](https://github.com/choldgraf))
- Update pre-commit to use Ruff; update versions and add a few rules [#137](https://github.com/executablebooks/github-activity/pull/137) ([@stefanv](https://github.com/stefanv), [@bsipocz](https://github.com/bsipocz))
- Change token to readonly PAT so we don't hit rate limits [#134](https://github.com/executablebooks/github-activity/pull/134) ([@choldgraf](https://github.com/choldgraf), [@bsipocz](https://github.com/bsipocz))
- Fix tests and move contributing docs into our docs [#133](https://github.com/executablebooks/github-activity/pull/133) ([@choldgraf](https://github.com/choldgraf))
- Update test suite to use fewer GitHub API calls [#144](https://github.com/executablebooks/github-activity/pull/144) ([@choldgraf](https://github.com/choldgraf), [@bsipocz](https://github.com/bsipocz), [@stefanv](https://github.com/stefanv))
- Bump actions/checkout from 5 to 6 in the actions group [#143](https://github.com/executablebooks/github-activity/pull/143) ([@bsipocz](https://github.com/bsipocz), [@dependabot[bot]](https://github.com/dependabot[bot]))
- Bump actions/checkout from 4 to 5 [#140](https://github.com/executablebooks/github-activity/pull/140) ([@bsipocz](https://github.com/bsipocz), [@dependabot[bot]](https://github.com/dependabot[bot]))
- Bump actions/setup-python from 5 to 6 [#139](https://github.com/executablebooks/github-activity/pull/139) ([@bsipocz](https://github.com/bsipocz), [@dependabot[bot]](https://github.com/dependabot[bot]))
- add pyproject.toml [#132](https://github.com/executablebooks/github-activity/pull/132) ([@minrk](https://github.com/minrk), [@choldgraf](https://github.com/choldgraf))
- [DOC] Clarify some intended functionality in docs [#127](https://github.com/executablebooks/github-activity/pull/127) ([@choldgraf](https://github.com/choldgraf), [@manics](https://github.com/manics))

### Documentation improvements

- make sure generated anchor links resolve [#122](https://github.com/executablebooks/github-activity/pull/122) ([@minrk](https://github.com/minrk), [@consideRatio](https://github.com/consideRatio))

### Contributors to this release

The following people contributed discussions, new ideas, code and documentation contributions, and review.
See [our definition of contributors](https://github-activity.readthedocs.io/en/latest/#how-does-this-tool-define-contributions-in-the-reports).

([GitHub contributors page for this release](https://github.com/executablebooks/github-activity/graphs/contributors?from=2025-04-11&to=2025-12-09&type=c))

@bsipocz ([activity](https://github.com/search?q=repo%3Aexecutablebooks%2Fgithub-activity+involves%3Absipocz+updated%3A2025-04-11..2025-12-09&type=Issues)) | @choldgraf ([activity](https://github.com/search?q=repo%3Aexecutablebooks%2Fgithub-activity+involves%3Acholdgraf+updated%3A2025-04-11..2025-12-09&type=Issues)) | @consideRatio ([activity](https://github.com/search?q=repo%3Aexecutablebooks%2Fgithub-activity+involves%3AconsideRatio+updated%3A2025-04-11..2025-12-09&type=Issues)) | @dependabot[bot] ([activity](https://github.com/search?q=repo%3Aexecutablebooks%2Fgithub-activity+involves%3Adependabot[bot]+updated%3A2025-04-11..2025-12-09&type=Issues)) | @jtpio ([activity](https://github.com/search?q=repo%3Aexecutablebooks%2Fgithub-activity+involves%3Ajtpio+updated%3A2025-04-11..2025-12-09&type=Issues)) | @manics ([activity](https://github.com/search?q=repo%3Aexecutablebooks%2Fgithub-activity+involves%3Amanics+updated%3A2025-04-11..2025-12-09&type=Issues)) | @minrk ([activity](https://github.com/search?q=repo%3Aexecutablebooks%2Fgithub-activity+involves%3Aminrk+updated%3A2025-04-11..2025-12-09&type=Issues)) | @nabobalis ([activity](https://github.com/search?q=repo%3Aexecutablebooks%2Fgithub-activity+involves%3Anabobalis+updated%3A2025-04-11..2025-12-09&type=Issues)) | @stefanv ([activity](https://github.com/search?q=repo%3Aexecutablebooks%2Fgithub-activity+involves%3Astefanv+updated%3A2025-04-11..2025-12-09&type=Issues))

## v1.0.3 - 2025-04-12

### Continuous integration improvements

- ci: fix github action tag in publish workflow [#119](https://github.com/executablebooks/github-activity/pull/119) ([@consideRatio](https://github.com/consideRatio))
- ci: fix location of dependabot.yaml [#118](https://github.com/executablebooks/github-activity/pull/118) ([@consideRatio](https://github.com/consideRatio))

## v1.0.2 - 2025-04-12

### Continuous integration improvements

- Fix another issue in the publish workflow [#116](https://github.com/executablebooks/github-activity/pull/116) ([@consideRatio](https://github.com/consideRatio))

## v1.0.1 - 2025-04-11

### Continuous integration improvements

- Fix publish workflow failure [#114](https://github.com/executablebooks/github-activity/pull/114) ([@consideRatio](https://github.com/consideRatio))

## v1.0.0 - 2025-04-11

### New features added

- Parse target as an optional positional argument [#94](https://github.com/executablebooks/github-activity/pull/94) ([@manics](https://github.com/manics), [@choldgraf](https://github.com/choldgraf))
- Load argument defaults from `.githubactivity.json` [#93](https://github.com/executablebooks/github-activity/pull/93) ([@manics](https://github.com/manics), [@consideRatio](https://github.com/consideRatio))
- Add a continuous integration category [#92](https://github.com/executablebooks/github-activity/pull/92) ([@consideRatio](https://github.com/consideRatio), [@choldgraf](https://github.com/choldgraf))
- accept 'breaking' label for breaking changes [#90](https://github.com/executablebooks/github-activity/pull/90) ([@minrk](https://github.com/minrk), [@choldgraf](https://github.com/choldgraf))
- Make github friendly outputs [#82](https://github.com/executablebooks/github-activity/pull/82) ([@choldgraf](https://github.com/choldgraf), [@minrk](https://github.com/minrk))

### Enhancements made

- exclude bot users from all contributors list [#87](https://github.com/executablebooks/github-activity/pull/87) ([@minrk](https://github.com/minrk), [@choldgraf](https://github.com/choldgraf), [@consideRatio](https://github.com/consideRatio))
- ENH: Write messages about GH token to stderr [#83](https://github.com/executablebooks/github-activity/pull/83) ([@minrk](https://github.com/minrk), [@choldgraf](https://github.com/choldgraf))
- [ENH] include reviewers and committers in contributor list [#65](https://github.com/executablebooks/github-activity/pull/65) ([@minrk](https://github.com/minrk), [@choldgraf](https://github.com/choldgraf))

### Bugs fixed

- apply token via auth adapter [#98](https://github.com/executablebooks/github-activity/pull/98) ([@minrk](https://github.com/minrk), [@consideRatio](https://github.com/consideRatio))
- fix encoding when getting token from gh cli [#97](https://github.com/executablebooks/github-activity/pull/97) ([@minrk](https://github.com/minrk), [@consideRatio](https://github.com/consideRatio))
- fix token retrieval from gh cli [#89](https://github.com/executablebooks/github-activity/pull/89) ([@minrk](https://github.com/minrk), [@choldgraf](https://github.com/choldgraf))
- ENH: Write messages about GH token to stderr [#83](https://github.com/executablebooks/github-activity/pull/83) ([@minrk](https://github.com/minrk), [@choldgraf](https://github.com/choldgraf))

### Maintenance and upkeep improvements

- Require Python 3.9+ [#111](https://github.com/executablebooks/github-activity/pull/111) ([@consideRatio](https://github.com/consideRatio), [@choldgraf](https://github.com/choldgraf))
- Update tests to work against new github URL for jupyter-book [#109](https://github.com/executablebooks/github-activity/pull/109) ([@consideRatio](https://github.com/consideRatio))
- Fix ReadTheDocs config - specifying conf location is required [#108](https://github.com/executablebooks/github-activity/pull/108) ([@consideRatio](https://github.com/consideRatio))
- Add dependabot to bump github actions, and bump them [#107](https://github.com/executablebooks/github-activity/pull/107) ([@consideRatio](https://github.com/consideRatio))
- Fix detail in readthedocs config [#106](https://github.com/executablebooks/github-activity/pull/106) ([@consideRatio](https://github.com/consideRatio))
- Install required docs/test dependencies when using nox [#105](https://github.com/executablebooks/github-activity/pull/105) ([@consideRatio](https://github.com/consideRatio))
- avoid deprecated `pandas.value_counts` [#102](https://github.com/executablebooks/github-activity/pull/102) ([@minrk](https://github.com/minrk), [@consideRatio](https://github.com/consideRatio))
- Add repository URL to project metadata [#101](https://github.com/executablebooks/github-activity/pull/101) ([@mfisher87](https://github.com/mfisher87), [@choldgraf](https://github.com/choldgraf))

### Documentation improvements

- docs: backfill changelog [#112](https://github.com/executablebooks/github-activity/pull/112) ([@consideRatio](https://github.com/consideRatio))
- Overhaul documentation and add contributing guide [#86](https://github.com/executablebooks/github-activity/pull/86) ([@choldgraf](https://github.com/choldgraf), [@blink1073](https://github.com/blink1073), [@manics](https://github.com/manics), [@minrk](https://github.com/minrk))

### Continuous integration improvements

- ci: test with latest python version as well [#110](https://github.com/executablebooks/github-activity/pull/110) ([@consideRatio](https://github.com/consideRatio))
- ci: run pytest with color and more details [#103](https://github.com/executablebooks/github-activity/pull/103) ([@consideRatio](https://github.com/consideRatio))

### Contributors to this release

The following people contributed discussions, new ideas, code and documentation contributions, and review.
See [our definition of contributors](https://github-activity.readthedocs.io/en/latest/#how-does-this-tool-define-contributions-in-the-reports).

([GitHub contributors page for this release](https://github.com/executablebooks/github-activity/graphs/contributors?from=2023-02-13&to=2025-04-11&type=c))

@blink1073 ([activity](https://github.com/search?q=repo%3Aexecutablebooks%2Fgithub-activity+involves%3Ablink1073+updated%3A2023-02-13..2025-04-11&type=Issues)) | @choldgraf ([activity](https://github.com/search?q=repo%3Aexecutablebooks%2Fgithub-activity+involves%3Acholdgraf+updated%3A2023-02-13..2025-04-11&type=Issues)) | @consideRatio ([activity](https://github.com/search?q=repo%3Aexecutablebooks%2Fgithub-activity+involves%3AconsideRatio+updated%3A2023-02-13..2025-04-11&type=Issues)) | @manics ([activity](https://github.com/search?q=repo%3Aexecutablebooks%2Fgithub-activity+involves%3Amanics+updated%3A2023-02-13..2025-04-11&type=Issues)) | @mfisher87 ([activity](https://github.com/search?q=repo%3Aexecutablebooks%2Fgithub-activity+involves%3Amfisher87+updated%3A2023-02-13..2025-04-11&type=Issues)) | @minrk ([activity](https://github.com/search?q=repo%3Aexecutablebooks%2Fgithub-activity+involves%3Aminrk+updated%3A2023-02-13..2025-04-11&type=Issues)) | @wolfv ([activity](https://github.com/search?q=repo%3Aexecutablebooks%2Fgithub-activity+involves%3Awolfv+updated%3A2023-02-13..2025-04-11&type=Issues))

## v0.3.0 - 2023-02-13

### New features added

- Add ability to use GH CLI Authentication [#66](https://github.com/executablebooks/github-activity/pull/66) ([@choldgraf](https://github.com/choldgraf))

### Enhancements made

- [ENH] Add a bootstrap function for all changelog entries [#64](https://github.com/executablebooks/github-activity/pull/64) ([@blink1073](https://github.com/blink1073), [@choldgraf](https://github.com/choldgraf), [@jtpio](https://github.com/jtpio))

### Bugs fixed

- BUG: import dateutil.parser [#73](https://github.com/executablebooks/github-activity/pull/73) ([@agoose77](https://github.com/agoose77), [@consideRatio](https://github.com/consideRatio), [@choldgraf](https://github.com/choldgraf))

### Maintenance and upkeep improvements

- MAINT: Add check for installed gh cli [#72](https://github.com/executablebooks/github-activity/pull/72) ([@choldgraf](https://github.com/choldgraf), [@stefanv](https://github.com/stefanv))

### Contributors to this release

The following people contributed discussions, new ideas, code and documentation contributions, and review.
See [our definition of contributors](https://github-activity.readthedocs.io/en/latest/#how-does-this-tool-define-contributions-in-the-reports).

([GitHub contributors page for this release](https://github.com/executablebooks/github-activity/graphs/contributors?from=2021-12-01&to=2023-02-13&type=c))

@agoose77 ([activity](https://github.com/search?q=repo%3Aexecutablebooks%2Fgithub-activity+involves%3Aagoose77+updated%3A2021-12-01..2023-02-13&type=Issues)) | @blink1073 ([activity](https://github.com/search?q=repo%3Aexecutablebooks%2Fgithub-activity+involves%3Ablink1073+updated%3A2021-12-01..2023-02-13&type=Issues)) | @choldgraf ([activity](https://github.com/search?q=repo%3Aexecutablebooks%2Fgithub-activity+involves%3Acholdgraf+updated%3A2021-12-01..2023-02-13&type=Issues)) | @consideRatio ([activity](https://github.com/search?q=repo%3Aexecutablebooks%2Fgithub-activity+involves%3AconsideRatio+updated%3A2021-12-01..2023-02-13&type=Issues)) | @jtpio ([activity](https://github.com/search?q=repo%3Aexecutablebooks%2Fgithub-activity+involves%3Ajtpio+updated%3A2021-12-01..2023-02-13&type=Issues)) | @stefanv ([activity](https://github.com/search?q=repo%3Aexecutablebooks%2Fgithub-activity+involves%3Astefanv+updated%3A2021-12-01..2023-02-13&type=Issues))

## v0.2.0 - 2021-12-01

### Enhancements made

- Use auth for all usages of requests [#60](https://github.com/executablebooks/github-activity/pull/60) ([@blink1073](https://github.com/blink1073), [@choldgraf](https://github.com/choldgraf), [@consideRatio](https://github.com/consideRatio))
- Handle detection of target from SSH based remotes [#51](https://github.com/executablebooks/github-activity/pull/51) ([@consideRatio](https://github.com/consideRatio), [@choldgraf](https://github.com/choldgraf))
- ✨ ENH: Auto-detecting the target [#45](https://github.com/executablebooks/github-activity/pull/45) ([@choldgraf](https://github.com/choldgraf), [@consideRatio](https://github.com/consideRatio))

### Bugs fixed

- 🐛 FIX: write status messages to sys.stderr [#47](https://github.com/executablebooks/github-activity/pull/47) ([@minrk](https://github.com/minrk), [@choldgraf](https://github.com/choldgraf))

### Maintenance and upkeep improvements

- 🔧 MAINT: Split test_cli using @pytest.mark.parameterize [#56](https://github.com/executablebooks/github-activity/pull/56) ([@manics](https://github.com/manics), [@choldgraf](https://github.com/choldgraf))
- pre-commit configured and executed [#55](https://github.com/executablebooks/github-activity/pull/55) ([@consideRatio](https://github.com/consideRatio), [@choldgraf](https://github.com/choldgraf))
- 🔧 MAINT: \_get_latest_tag should use the remote repo [#52](https://github.com/executablebooks/github-activity/pull/52) ([@manics](https://github.com/manics), [@consideRatio](https://github.com/consideRatio))
- 🔧 MAINT: hyphen instead of asterisk [#44](https://github.com/executablebooks/github-activity/pull/44) ([@choldgraf](https://github.com/choldgraf))

### Contributors to this release

The following people contributed discussions, new ideas, code and documentation contributions, and review.
See [our definition of contributors](https://github-activity.readthedocs.io/en/latest/#how-does-this-tool-define-contributions-in-the-reports).

([GitHub contributors page for this release](https://github.com/executablebooks/github-activity/graphs/contributors?from=2021-02-20&to=2021-12-01&type=c))

@blink1073 ([activity](https://github.com/search?q=repo%3Aexecutablebooks%2Fgithub-activity+involves%3Ablink1073+updated%3A2021-02-20..2021-12-01&type=Issues)) | @choldgraf ([activity](https://github.com/search?q=repo%3Aexecutablebooks%2Fgithub-activity+involves%3Acholdgraf+updated%3A2021-02-20..2021-12-01&type=Issues)) | @consideRatio ([activity](https://github.com/search?q=repo%3Aexecutablebooks%2Fgithub-activity+involves%3AconsideRatio+updated%3A2021-02-20..2021-12-01&type=Issues)) | @manics ([activity](https://github.com/search?q=repo%3Aexecutablebooks%2Fgithub-activity+involves%3Amanics+updated%3A2021-02-20..2021-12-01&type=Issues)) | @minrk ([activity](https://github.com/search?q=repo%3Aexecutablebooks%2Fgithub-activity+involves%3Aminrk+updated%3A2021-02-20..2021-12-01&type=Issues)) | @wolfv ([activity](https://github.com/search?q=repo%3Aexecutablebooks%2Fgithub-activity+involves%3Awolfv+updated%3A2021-02-20..2021-12-01&type=Issues))

## v0.1.3 - 2021-02-20

### New features added

- Adding filtering by branch [#42](https://github.com/executablebooks/github-activity/pull/42) ([@choldgraf](https://github.com/choldgraf), [@blink1073](https://github.com/blink1073), [@consideRatio](https://github.com/consideRatio))
- ✨NEW: heading_level argument for increasing heading level [#38](https://github.com/executablebooks/github-activity/pull/38) ([@minrk](https://github.com/minrk), [@choldgraf](https://github.com/choldgraf), [@consideRatio](https://github.com/consideRatio))

### Enhancements made

- use tqdm for progress [#39](https://github.com/executablebooks/github-activity/pull/39) ([@minrk](https://github.com/minrk), [@choldgraf](https://github.com/choldgraf), [@consideRatio](https://github.com/consideRatio))
- 👌IMPROVE: add blank lines below headings [#36](https://github.com/executablebooks/github-activity/pull/36) ([@minrk](https://github.com/minrk), [@choldgraf](https://github.com/choldgraf))
- 👌 IMPROVE: since/until: assume git reference, fallback to datetime [#33](https://github.com/executablebooks/github-activity/pull/33) ([@consideRatio](https://github.com/consideRatio), [@choldgraf](https://github.com/choldgraf))

### Bugs fixed

- 🐛 FIX: tags like 'doctor' would trigger 'doc' tag [#40](https://github.com/executablebooks/github-activity/pull/40) ([@consideRatio](https://github.com/consideRatio), [@choldgraf](https://github.com/choldgraf))

### Maintenance and upkeep improvements

- Remove no longer used code [#37](https://github.com/executablebooks/github-activity/pull/37) ([@consideRatio](https://github.com/consideRatio), [@choldgraf](https://github.com/choldgraf))
- [FIX,TST] resolve refs when not run from a repo [#35](https://github.com/executablebooks/github-activity/pull/35) ([@minrk](https://github.com/minrk), [@choldgraf](https://github.com/choldgraf), [@consideRatio](https://github.com/consideRatio))

### Documentation improvements

- 📚 DOC: Minor docs changes [#43](https://github.com/executablebooks/github-activity/pull/43) ([@choldgraf](https://github.com/choldgraf))

### Contributors to this release

The following people contributed discussions, new ideas, code and documentation contributions, and review.
See [our definition of contributors](https://github-activity.readthedocs.io/en/latest/#how-does-this-tool-define-contributions-in-the-reports).

([GitHub contributors page for this release](https://github.com/executablebooks/github-activity/graphs/contributors?from=2020-08-31&to=2021-02-20&type=c))

@blink1073 ([activity](https://github.com/search?q=repo%3Aexecutablebooks%2Fgithub-activity+involves%3Ablink1073+updated%3A2020-08-31..2021-02-20&type=Issues)) | @choldgraf ([activity](https://github.com/search?q=repo%3Aexecutablebooks%2Fgithub-activity+involves%3Acholdgraf+updated%3A2020-08-31..2021-02-20&type=Issues)) | @consideRatio ([activity](https://github.com/search?q=repo%3Aexecutablebooks%2Fgithub-activity+involves%3AconsideRatio+updated%3A2020-08-31..2021-02-20&type=Issues)) | @minrk ([activity](https://github.com/search?q=repo%3Aexecutablebooks%2Fgithub-activity+involves%3Aminrk+updated%3A2020-08-31..2021-02-20&type=Issues))

## v0.1.2 - 2020-08-31

### Maintenance and upkeep improvements

- adding thumbsup to query [#31](https://github.com/executablebooks/github-activity/pull/31) ([@choldgraf](https://github.com/choldgraf))

### Contributors to this release

The following people contributed discussions, new ideas, code and documentation contributions, and review.
See [our definition of contributors](https://github-activity.readthedocs.io/en/latest/#how-does-this-tool-define-contributions-in-the-reports).

([GitHub contributors page for this release](https://github.com/executablebooks/github-activity/graphs/contributors?from=2020-08-07&to=2020-08-31&type=c))

@choldgraf ([activity](https://github.com/search?q=repo%3Aexecutablebooks%2Fgithub-activity+involves%3Acholdgraf+updated%3A2020-08-07..2020-08-31&type=Issues))

## v0.1.1 - 2020-08-07

### New features added

- ✨ NEW: add support for title prefixes [#30](https://github.com/executablebooks/github-activity/pull/30) ([@choldgraf](https://github.com/choldgraf))
- Tests and URL CLI option [#25](https://github.com/executablebooks/github-activity/pull/25) ([@choldgraf](https://github.com/choldgraf))

### Enhancements made

- Fail early on missing GitHub api credentials [#27](https://github.com/executablebooks/github-activity/pull/27) ([@consideRatio](https://github.com/consideRatio), [@choldgraf](https://github.com/choldgraf))

### Documentation improvements

- documentation [#26](https://github.com/executablebooks/github-activity/pull/26) ([@choldgraf](https://github.com/choldgraf))

### Contributors to this release

The following people contributed discussions, new ideas, code and documentation contributions, and review.
See [our definition of contributors](https://github-activity.readthedocs.io/en/latest/#how-does-this-tool-define-contributions-in-the-reports).

([GitHub contributors page for this release](https://github.com/executablebooks/github-activity/graphs/contributors?from=2020-04-25&to=2020-08-07&type=c))

@choldgraf ([activity](https://github.com/search?q=repo%3Aexecutablebooks%2Fgithub-activity+involves%3Acholdgraf+updated%3A2020-04-25..2020-08-07&type=Issues)) | @consideRatio ([activity](https://github.com/search?q=repo%3Aexecutablebooks%2Fgithub-activity+involves%3AconsideRatio+updated%3A2020-04-25..2020-08-07&type=Issues))

## v0.1.0 - 2020-04-25

### New features added

- adding contributors list [#10](https://github.com/executablebooks/github-activity/pull/10) ([@choldgraf](https://github.com/choldgraf), [@consideRatio](https://github.com/consideRatio))
- Support git references etc. [#6](https://github.com/executablebooks/github-activity/pull/6) ([@consideRatio](https://github.com/consideRatio), [@choldgraf](https://github.com/choldgraf))

### Enhancements made

- adding simple cacheing functionality [#24](https://github.com/executablebooks/github-activity/pull/24) ([@choldgraf](https://github.com/choldgraf), [@consideRatio](https://github.com/consideRatio))
- defining contributions [#14](https://github.com/executablebooks/github-activity/pull/14) ([@choldgraf](https://github.com/choldgraf), [@betatim](https://github.com/betatim))
- updating CLI for new tags [#12](https://github.com/executablebooks/github-activity/pull/12) ([@choldgraf](https://github.com/choldgraf))
- some improvements to `since` and opened issues list [#8](https://github.com/executablebooks/github-activity/pull/8) ([@choldgraf](https://github.com/choldgraf), [@consideRatio](https://github.com/consideRatio))

### Bugs fixed

- Handle @ghost authors of comments [#16](https://github.com/executablebooks/github-activity/pull/16) ([@consideRatio](https://github.com/consideRatio), [@choldgraf](https://github.com/choldgraf))
- fixing link to changelog with refs [#11](https://github.com/executablebooks/github-activity/pull/11) ([@choldgraf](https://github.com/choldgraf))

### Maintenance and upkeep improvements

- Remove details on what a contributor is [#19](https://github.com/executablebooks/github-activity/pull/19) ([@betatim](https://github.com/betatim), [@choldgraf](https://github.com/choldgraf))
- adding authentication information [#2](https://github.com/executablebooks/github-activity/pull/2) ([@choldgraf](https://github.com/choldgraf))

### Documentation improvements

- Mention the required GITHUB_ACCESS_TOKEN [#1](https://github.com/executablebooks/github-activity/pull/1) ([@consideRatio](https://github.com/consideRatio), [@choldgraf](https://github.com/choldgraf))

### Contributors to this release

The following people contributed discussions, new ideas, code and documentation contributions, and review.
See [our definition of contributors](https://github-activity.readthedocs.io/en/latest/#how-does-this-tool-define-contributions-in-the-reports).

([GitHub contributors page for this release](https://github.com/executablebooks/github-activity/graphs/contributors?from=2015-01-01&to=2020-04-25&type=c))

@betatim ([activity](https://github.com/search?q=repo%3Aexecutablebooks%2Fgithub-activity+involves%3Abetatim+updated%3A2015-01-01..2020-04-25&type=Issues)) | @choldgraf ([activity](https://github.com/search?q=repo%3Aexecutablebooks%2Fgithub-activity+involves%3Acholdgraf+updated%3A2015-01-01..2020-04-25&type=Issues)) | @consideRatio ([activity](https://github.com/search?q=repo%3Aexecutablebooks%2Fgithub-activity+involves%3AconsideRatio+updated%3A2015-01-01..2020-04-25&type=Issues))
