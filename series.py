SERIES = {
    "1": {
        "name": "Dragon Ball",
        "total_episodes": 153,
        "filename_pattern": (
            r"^Dragon Ball\s*-\s*S\d+E(?P<episode>\d{3})"
            r"\s*-\s*(?P<title>.+)$"
        ),
        "seasons": [
            {"season": 1, "start": 1, "end": 153},
        ],
        "keep_title": True,
    },
    "2": {
        "name": "Dragon Ball Z",
        "total_episodes": 291,
        "filename_pattern": (
            r"^DBZ_Episodio\s+(?P<episode>\d{3})"
        ),
        "seasons": [
            {"season": 1, "start": 1, "end": 39},
            {"season": 2, "start": 40, "end": 74},
            {"season": 3, "start": 75, "end": 107},
            {"season": 4, "start": 108, "end": 139},
            {"season": 5, "start": 140, "end": 165},
            {"season": 6, "start": 166, "end": 194},
            {"season": 7, "start": 195, "end": 219},
            {"season": 8, "start": 220, "end": 253},
            {"season": 9, "start": 254, "end": 291},
        ],
        "keep_title": False,
    },
}