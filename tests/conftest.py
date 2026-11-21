import os

import pytest

# The weekly live-api workflow sets this to run the tests against the real GitHub API
LIVE_TESTS = bool(os.environ.get("GITHUB_ACTIVITY_LIVE_TESTS"))


@pytest.fixture(scope="session")
def vcr_config():
    config = {
        # Never write tokens into the cassettes
        "filter_headers": ["authorization"],
        # Every GraphQL request POSTs to the same URL, so the body must match too
        "match_on": ["method", "scheme", "host", "path", "query", "body"],
        "decode_compressed_response": True,
    }
    if LIVE_TESTS:
        # Many tests make identical requests, replaying them keeps the run
        # within the GITHUB_TOKEN rate limit
        config["allow_playback_repeats"] = True
    return config


if LIVE_TESTS:
    # Record every test into one throwaway cassette, so only requests that
    # haven't been made yet in this run reach GitHub

    @pytest.fixture(scope="session")
    def record_mode():
        return "new_episodes"

    @pytest.fixture(scope="session")
    def vcr_cassette_dir(tmp_path_factory):
        return str(tmp_path_factory.mktemp("cassettes"))

    @pytest.fixture
    def default_cassette_name():
        return "live"


@pytest.fixture(autouse=True)
def github_token(monkeypatch):
    """Replaying cassettes needs no real token, but the code refuses to run without one."""
    if not (os.environ.get("GITHUB_ACCESS_TOKEN") or os.environ.get("GITHUB_TOKEN")):
        monkeypatch.setenv("GITHUB_ACCESS_TOKEN", "dummy-token")
