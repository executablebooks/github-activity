# Changelog

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
