VIDEO_EXTENSIONS = {
    ".avi",
    ".mkv",
    ".mp4",
    ".m4v",
    ".mov",
    ".rmvb",
    ".webm",
}


FILENAME_PATTERNS = {
    "season_episode": (
        r"^.*?"
        r"S(?P<season>\d{1,2})"
        r"E(?P<start>\d{1,3})"
        r"(?:[-_](?:E)?(?P<end>\d{1,3}))?"
        r"(?:\s*-\s*(?P<title>.+))?$"
    ),

    "absolute_episode": (
        r"^.*?\s+(?P<start>\d{1,3})$"
    ),
}


def season_series(
    name: str,
    folder_names: list[str],
    expected_by_season: dict[int, set[int]] | None = None,
    keep_title: bool = False,
    filename_patterns: list[str] | None = None,
    enabled: bool = True,
    note: str = "",
) -> dict:
    return {
        "name": name,
        "folder_names": folder_names,
        "numbering_mode": "season",
        "filename_patterns": (
            filename_patterns
            if filename_patterns is not None
            else [FILENAME_PATTERNS["season_episode"]]
        ),
        "expected_by_season": expected_by_season,
        "keep_title": keep_title,
        "keep_absolute_number": False,
        "episode_digits": 2,
        "enabled": enabled,
        "note": note,
    }


def absolute_series(
    name: str,
    folder_names: list[str],
    total_episodes: int | None,
    seasons: list[dict],
    filename_patterns: list[str] | None = None,
    keep_title: bool = False,
    keep_absolute_number: bool = False,
    episode_digits: int = 3,
    enabled: bool = True,
    note: str = "",
) -> dict:
    return {
        "name": name,
        "folder_names": folder_names,
        "numbering_mode": "absolute",
        "filename_patterns": (
            filename_patterns
            if filename_patterns is not None
            else [FILENAME_PATTERNS["absolute_episode"]]
        ),
        "total_episodes": total_episodes,
        "seasons": seasons,
        "keep_title": keep_title,
        "keep_absolute_number": keep_absolute_number,
        "episode_digits": episode_digits,
        "enabled": enabled,
        "note": note,
    }