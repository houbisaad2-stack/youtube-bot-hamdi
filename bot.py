import json
import logging
import os

from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def _extract_refresh_token(token_value: str):
    """Accept either a raw refresh token or a JSON credential blob."""
    if not token_value:
        return None

    token_value = token_value.strip()

    if not (token_value.startswith("{") and token_value.endswith("}")):
        return token_value

    try:
        data = json.loads(token_value)
    except json.JSONDecodeError:
        return token_value

    if isinstance(data, dict):
        if isinstance(data.get("refresh_token"), str):
            return data["refresh_token"]

        for key in ("installed", "web"):
            nested = data.get(key)
            if isinstance(nested, dict) and isinstance(nested.get("refresh_token"), str):
                return nested["refresh_token"]

    return None


def get_youtube_service():
    client_id = os.environ.get("YOUTUBE_CLIENT_ID")
    client_secret = os.environ.get("YOUTUBE_CLIENT_SECRET")
    token_secret = os.environ.get("YOUTUBE_TOKEN")

    missing = [
        name for name, value in (
            ("YOUTUBE_CLIENT_ID", client_id),
            ("YOUTUBE_CLIENT_SECRET", client_secret),
            ("YOUTUBE_TOKEN", token_secret),
        ) if not value
    ]
    if missing:
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

    refresh_token = _extract_refresh_token(token_secret)
    if not refresh_token:
        raise ValueError(
            "YOUTUBE_TOKEN does not contain a valid refresh token. "
            "Use the OAuth refresh token itself or a JSON credential blob with a refresh_token field."
        )

    creds = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
        scopes=["https://www.googleapis.com/auth/youtube.upload"],
    )

    try:
        if not creds.valid:
            logging.info("Refreshing YouTube access token...")
            creds.refresh(Request())
    except RefreshError as exc:
        raise RuntimeError(
            "Authentication failed while refreshing the YouTube access token. "
            "Verify that YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, and YOUTUBE_TOKEN are all correct and belong to the same OAuth client."
        ) from exc

    return build("youtube", "v3", credentials=creds, cache_discovery=False)


if __name__ == "__main__":
    try:
        get_youtube_service()
        print("✅ Connected to YouTube API and refreshed the access token successfully.")
    except Exception as exc:
        logging.error("Error while connecting to YouTube API: %s", exc)
        print(f"❌ Error: {exc}")
        print(
            "Hints:\n"
            "- YOUTUBE_TOKEN must be the OAuth refresh token, not an access token.\n"
            "- If you stored a JSON credential blob, it must include a refresh_token field.\n"
            "- Make sure YOUTUBE_CLIENT_ID and YOUTUBE_CLIENT_SECRET match the OAuth app used to generate the refresh token."
        )
