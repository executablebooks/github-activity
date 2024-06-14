from requests.auth import AuthBase


class TokenAuth(AuthBase):
    """Apply Bearer token auth to request

    Requests doesn't respect Authorization header reliably
    unless applied via `auth` adapter.
    """

    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        # add token to auth
        r.headers["Authorization"] = f"Bearer {self.token}"
        return r
