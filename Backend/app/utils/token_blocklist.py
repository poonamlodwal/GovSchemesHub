_BLOCKLIST = set()


def add_token_to_blocklist(jti):
    """Mark a token's jti as revoked (used on logout)."""
    _BLOCKLIST.add(jti)


def is_token_revoked(jti):
    """Return True if the given jti has been revoked."""
    return jti in _BLOCKLIST
