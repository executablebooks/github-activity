## v0.2.0

([full changelog](https://github.com/executablebooks/github-activity/compare/ca2819b...f994a69))

### Enhancements made

- Use auth for all usages of requests [#60](https://github.com/executablebooks/github-activity/pull/60) ([@blink1073](https://github.com/blink1073), [@choldgraf](https://github.com/choldgraf), [@consideRatio](https://github.com/consideRatio))
- Handle detection of target from SSH based remotes [#51](https://github.com/executablebooks/github-activity/pull/51) ([@choldgraf](https://github.com/choldgraf), [@consideRatio](https://github.com/consideRatio))
- ✨ ENH: Auto-detecting the target [#45](https://github.com/executablebooks/github-activity/pull/45) ([@choldgraf](https://github.com/choldgraf), [@consideRatio](https://github.com/consideRatio))

### Bugs fixed

- 🐛 FIX: write status messages to sys.stderr [#47](https://github.com/executablebooks/github-activity/pull/47) ([@choldgraf](https://github.com/choldgraf), [@minrk](https://github.com/minrk))

### Maintenance and upkeep improvements

- 🔧 MAINT: Split test_cli using @pytest.mark.parameterize [#56](https://github.com/executablebooks/github-activity/pull/56) ([@choldgraf](https://github.com/choldgraf), [@manics](https://github.com/manics))
- pre-commit configured and executed [#55](https://github.com/executablebooks/github-activity/pull/55) ([@choldgraf](https://github.com/choldgraf), [@consideRatio](https://github.com/consideRatio))
- 🔧 MAINT: _get_latest_tag should use the remote repo [#52](https://github.com/executablebooks/github-activity/pull/52) ([@consideRatio](https://github.com/consideRatio), [@manics](https://github.com/manics))
- 🔧 MAINT: hyphen instead of asterisk [#44](https://github.com/executablebooks/github-activity/pull/44) ([@choldgraf](https://github.com/choldgraf))

### Contributors to this release

The following people contributed discussions, new ideas, code and documentation contributions, and review.
See [our definition of contributors](https://github-activity.readthedocs.io/en/latest/#how-does-this-tool-define-contributions-in-the-reports).

([GitHub contributors page for this release](https://github.com/executablebooks/github-activity/graphs/contributors?from=2021-02-20&to=2021-12-01&type=c))

@blink1073 ([activity](https://github.com/search?q=repo%3Aexecutablebooks%2Fgithub-activity+involves%3Ablink1073+updated%3A2021-02-20..2021-12-01&type=Issues)) | @choldgraf ([activity](https://github.com/search?q=repo%3Aexecutablebooks%2Fgithub-activity+involves%3Acholdgraf+updated%3A2021-02-20..2021-12-01&type=Issues)) | @consideRatio ([activity](https://github.com/search?q=repo%3Aexecutablebooks%2Fgithub-activity+involves%3AconsideRatio+updated%3A2021-02-20..2021-12-01&type=Issues)) | @manics ([activity](https://github.com/search?q=repo%3Aexecutablebooks%2Fgithub-activity+involves%3Amanics+updated%3A2021-02-20..2021-12-01&type=Issues)) | @minrk ([activity](https://github.com/search?q=repo%3Aexecutablebooks%2Fgithub-activity+involves%3Aminrk+updated%3A2021-02-20..2021-12-01&type=Issues)) | @wolfv ([activity](https://github.com/search?q=repo%3Aexecutablebooks%2Fgithub-activity+involves%3Awolfv+updated%3A2021-02-20..2021-12-01&type=Issues))

## v0.1.3

([full changelog](https://github.com/executablebooks/github-activity/compare/60c7f06...ca2819b))

### New features added

- Adding filtering by branch [#42](https://github.com/executablebooks/github-activity/pull/42) ([@blink1073](https://github.com/blink1073), [@choldgraf](https://github.com/choldgraf), [@consideRatio](https://github.com/consideRatio))
- ✨NEW: heading_level argument for increasing heading level [#38](https://github.com/executablebooks/github-activity/pull/38) ([@choldgraf](https://github.com/choldgraf), [@consideRatio](https://github.com/consideRatio), [@minrk](https://github.com/minrk))

### Enhancements made

- use tqdm for progress [#39](https://github.com/executablebooks/github-activity/pull/39) ([@choldgraf](https://github.com/choldgraf), [@consideRatio](https://github.com/consideRatio), [@minrk](https://github.com/minrk))
- 👌IMPROVE: add blank lines below headings [#36](https://github.com/executablebooks/github-activity/pull/36) ([@choldgraf](https://github.com/choldgraf), [@minrk](https://github.com/minrk))
- 👌 IMPROVE: since/until: assume git reference, fallback to datetime [#33](https://github.com/executablebooks/github-activity/pull/33) ([@choldgraf](https://github.com/choldgraf), [@consideRatio](https://github.com/consideRatio))

### Bugs fixed

- 🐛 FIX: tags like 'doctor' would trigger 'doc' tag [#40](https://github.com/executablebooks/github-activity/pull/40) ([@choldgraf](https://github.com/choldgraf), [@consideRatio](https://github.com/consideRatio))

### Maintenance and upkeep improvements

- Remove no longer used code [#37](https://github.com/executablebooks/github-activity/pull/37) ([@choldgraf](https://github.com/choldgraf), [@consideRatio](https://github.com/consideRatio))
- [FIX,TST] resolve refs when not run from a repo [#35](https://github.com/executablebooks/github-activity/pull/35) ([@choldgraf](https://github.com/choldgraf), [@consideRatio](https://github.com/consideRatio), [@minrk](https://github.com/minrk))

### Documentation improvements

- 📚 DOC: Minor docs changes [#43](https://github.com/executablebooks/github-activity/pull/43) ([@choldgraf](https://github.com/choldgraf))

### Contributors to this release

The following people contributed discussions, new ideas, code and documentation contributions, and review.
See [our definition of contributors](https://github-activity.readthedocs.io/en/latest/#how-does-this-tool-define-contributions-in-the-reports).

([GitHub contributors page for this release](https://github.com/executablebooks/github-activity/graphs/contributors?from=2020-08-31&to=2021-02-20&type=c))

@blink1073 ([activity](https://github.com/search?q=repo%3Aexecutablebooks%2Fgithub-activity+involves%3Ablink1073+updated%3A2020-08-31..2021-02-20&type=Issues)) | @choldgraf ([activity](https://github.com/search?q=repo%3Aexecutablebooks%2Fgithub-activity+involves%3Acholdgraf+updated%3A2020-08-31..2021-02-20&type=Issues)) | @consideRatio ([activity](https://github.com/search?q=repo%3Aexecutablebooks%2Fgithub-activity+involves%3AconsideRatio+updated%3A2020-08-31..2021-02-20&type=Issues)) | @minrk ([activity](https://github.com/search?q=repo%3Aexecutablebooks%2Fgithub-activity+involves%3Aminrk+updated%3A2020-08-31..2021-02-20&type=Issues))

## v0.1.2

([full changelog](https://github.com/executablebooks/github-activity/compare/32f89fd...60c7f06))

### Maintenance and upkeep improvements

- adding thumbsup to query [#31](https://github.com/executablebooks/github-activity/pull/31) ([@choldgraf](https://github.com/choldgraf))

### Contributors to this release

The following people contributed discussions, new ideas, code and documentation contributions, and review.
See [our definition of contributors](https://github-activity.readthedocs.io/en/latest/#how-does-this-tool-define-contributions-in-the-reports).

([GitHub contributors page for this release](https://github.com/executablebooks/github-activity/graphs/contributors?from=2020-08-07&to=2020-08-31&type=c))

@choldgraf ([activity](https://github.com/search?q=repo%3Aexecutablebooks%2Fgithub-activity+involves%3Acholdgraf+updated%3A2020-08-07..2020-08-31&type=Issues))
