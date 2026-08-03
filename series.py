SERIES = {
    "1": {
        "name": "Another",
        "numbering_mode": "season",
        "filename_patterns": [
            (
                r"^Another\s+S(?P<season>\d+)"
                r"E(?P<start>\d+)"
                r"(?:[-_](?P<end>\d+))?"
                r"(?:\s*-\s*(?P<title>.+))?$"
            ),
        ],
        "expected_by_season": {
            0: {1},
            1: set(range(1, 13)),
        },
        "keep_title": True,
        "keep_absolute_number": False,
        "episode_digits": 2,
    },

    "2": {
        "name": "Bleach",
        "numbering_mode": "absolute",
        "total_episodes": 366,

        # O programa tenta cada padrão até encontrar um compatível.
        "filename_patterns": [
            # bleachPROJECT_-_Epi_52_53
            # bleach_project_-_epi_068-069
            # AnimesDown.Com_Bleach_Epi_21
            (
                r"^.*?Epi[_\s.-]*"
                r"(?P<start>\d{1,3})"
                r"(?:[_-](?P<end>\d{1,3}))?$"
            ),

            # Bleach - 17
            r"^Bleach\s*-\s*(?P<start>\d{1,3})$",

            # AnimesDown.Com_Bleach_014
            (
                r"^AnimesDown\.Com_Bleach_"
                r"(?P<start>\d{1,3})$"
            ),
        ],

        # Divisão usada para os 366 episódios da série original.
        "seasons": [
            {"season": 1, "start": 1, "end": 20},
            {"season": 2, "start": 21, "end": 41},
            {"season": 3, "start": 42, "end": 63},
            {"season": 4, "start": 64, "end": 91},
            {"season": 5, "start": 92, "end": 109},
            {"season": 6, "start": 110, "end": 131},
            {"season": 7, "start": 132, "end": 151},
            {"season": 8, "start": 152, "end": 167},
            {"season": 9, "start": 168, "end": 189},
            {"season": 10, "start": 190, "end": 205},
            {"season": 11, "start": 206, "end": 212},
            {"season": 12, "start": 213, "end": 229},
            {"season": 13, "start": 230, "end": 265},
            {"season": 14, "start": 266, "end": 316},
            {"season": 15, "start": 317, "end": 342},
            {"season": 16, "start": 343, "end": 366},
        ],

        "keep_title": False,
        "keep_absolute_number": True,
        "episode_digits": 2,
    },

    "3": {
        "name": "Dragon Ball",
        "numbering_mode": "absolute",
        "total_episodes": 153,
        "filename_patterns": [
            (
                r"^Dragon Ball\s*-\s*S\d+E"
                r"(?P<start>\d{3})"
                r"\s*-\s*(?P<title>.+)$"
            ),
        ],
        "seasons": [
            {"season": 1, "start": 1, "end": 153},
        ],
        "keep_title": True,
        "keep_absolute_number": False,
        "episode_digits": 3,
    },

    "4": {
        "name": "Dragon Ball Z",
        "numbering_mode": "absolute",
        "total_episodes": 291,
        "filename_patterns": [
            r"^DBZ_Episodio\s+(?P<start>\d{3})",
        ],
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
        "keep_absolute_number": True,
        "episode_digits": 3,
    },

    "5": {
        "name": "Hunter x Hunter",
        "numbering_mode": "absolute",
        "total_episodes": 148,
        "filename_patterns": [
            (
                r"^Hunter\s+X\s+Hunter\s+"
                r"(?P<start>\d{3})$"
            ),
        ],
        "seasons": [
            {"season": 1, "start": 1, "end": 148},
        ],
        "keep_title": False,
        "keep_absolute_number": False,
        "episode_digits": 3,
    },
}