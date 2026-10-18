
def get_authenticated_service():
    scopes = ["https://www.googleapis.com/auth/youtube.upload"]

    client_json = os.environ.get("YOUTUBE_CLIENT_JSON")
    token_json = os.environ.get("YOUTUBE_TOKEN_JSON")
    token_value = os.environ.get("YOUTUBE_TOKEN")

    client_id = os.environ.get("YOUTUBE_CLIENT_ID")
    client_secret = os.environ.get("YOUTUBE_CLIENT_SECRET")

    if client_json:
        client_data = json.loads(client_json)
        config = (
            client_data.get("installed")
            or client_data.get("web")
            or client_data
        )
        client_id = config.get("client_id", client_id)
        client_secret = config.get("client_secret", client_secret)

    refresh_token = None

    if token_json:
        refresh_token = _extract_refresh_token(token_json)
    elif token_value:
        refresh_token = _extract_refresh_token(token_value)

    if not all([client_id, client_secret, refresh_token]):
        raise ValueError(
            "Missing YouTube OAuth secrets. Check "
            "YOUTUBE_CLIENT_JSON, YOUTUBE_TOKEN_JSON, "
            "or YOUTUBE_CLIENT_ID / YOUTUBE_CLIENT_SECRET / "
            "YOUTUBE_TOKEN in GitHub Secrets."
        )

    creds = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
        scopes=scopes,
    )

    creds.refresh(Request())

    return build(
        "youtube",
        "v3",
        credentials=creds,
        cache_discovery=False,
    )
