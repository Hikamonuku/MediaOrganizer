from pathlib import Path
import json

import requests


BASE_URL = "https://api.themoviedb.org/3"


def load_tmdb_token() -> str:
    settings_path = (
        Path(__file__).resolve().parent.parent
        / "Data"
        / "settings.json"
    )

    if not settings_path.exists():
        raise FileNotFoundError(
            "Data/settings.json was not found."
        )

    with settings_path.open(
        "r",
        encoding="utf-8",
    ) as file:
        settings = json.load(file)

    token = settings.get("tmdb_token")

    if not token:
        raise ValueError(
            "TMDb token was not configured."
        )

    return token


def get_headers() -> dict[str, str]:
    return {
        "Authorization": (
            f"Bearer {load_tmdb_token()}"
        ),
        "Accept": "application/json",
    }


def search_tv_series(
    query: str,
    language: str = "pt-BR",
) -> list[dict]:
    query = query.strip()

    if not query:
        return []

    response = requests.get(
        f"{BASE_URL}/search/tv",
        headers=get_headers(),
        params={
            "query": query,
            "language": language,
            "include_adult": False,
            "page": 1,
        },
        timeout=20,
    )

    response.raise_for_status()

    data = response.json()

    return data.get("results", [])