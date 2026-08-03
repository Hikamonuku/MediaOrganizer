from database import FILENAME_PATTERNS


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


SERIES = {
    "Another": season_series(
        name="Another",
        folder_names=["Another"],
        expected_by_season={
            0: {1},
            1: set(range(1, 13)),
        },
        keep_title=True,
    ),

    "Assassination Classroom": season_series(
        name="Assassination Classroom",
        folder_names=["Assassination Classroom"],
        expected_by_season={
            1: set(range(1, 23)),
        },
        note=(
            "S1E00 and the Sample folder need "
            "separate/manual treatment."
        ),
    ),

    "Black Lagoon": season_series(
        name="Black Lagoon",
        folder_names=[
            "Black Lagoon",
            "Black lagoon",
        ],
        expected_by_season={
            0: {1, 2},
            1: set(range(1, 13)),
            2: set(range(1, 13)),
        },
    ),

    "Bleach": absolute_series(
        name="Bleach",
        folder_names=["Bleach"],
        total_episodes=366,
        filename_patterns=[
            FILENAME_PATTERNS["bleach_epi"],
            FILENAME_PATTERNS["bleach_simple"],
        ],
        seasons=[
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
        keep_absolute_number=True,
        enabled=False,
        note="Old, incomplete and ambiguous RMVB collection.",
    ),

    "Caverna do Dragão": season_series(
        name="Caverna do Dragão",
        folder_names=["Caverna do Dragão"],
        expected_by_season=None,
        keep_title=True,
        enabled=False,
        note="Episode numbering after E15 needs manual correction.",
    ),

    "Death Note": season_series(
        name="Death Note",
        folder_names=["Death Note"],
        expected_by_season={
            1: set(range(1, 38)),
        },
        keep_title=True,
    ),

    "Dr. Stone": season_series(
        name="Dr. Stone",
        folder_names=["Dr. Stone"],
        expected_by_season={
            1: set(range(1, 25)),
            2: set(range(1, 12)),
            3: set(range(1, 23)),
            4: set(range(1, 23)),
        },
    ),

    "Dragon Ball": absolute_series(
        name="Dragon Ball",
        folder_names=[
            "Dragon Ball",
            "Dragon Ball (1986)",
        ],
        total_episodes=153,
        filename_patterns=[
            (
                r"^Dragon Ball\s*-\s*"
                r"S\d+E(?P<start>\d{3})"
                r"\s*-\s*(?P<title>.+)$"
            ),
        ],
        seasons=[
            {"season": 1, "start": 1, "end": 153},
        ],
        keep_title=True,
        episode_digits=3,
    ),

    "Dragon Ball Z": absolute_series(
        name="Dragon Ball Z",
        folder_names=["Dragon Ball Z"],
        total_episodes=291,
        filename_patterns=[
            FILENAME_PATTERNS["dbz_old"],
            FILENAME_PATTERNS["dbz_organized"],
        ],
        seasons=[
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
        keep_absolute_number=True,
        episode_digits=2,
    ),

    "Ergo Proxy": absolute_series(
        name="Ergo Proxy",
        folder_names=["Ergo Proxy"],
        total_episodes=23,
        seasons=[
            {"season": 1, "start": 1, "end": 23},
        ],
    ),

    "Gakuen Babysitters": season_series(
        name="Gakuen Babysitters",
        folder_names=["Gakuen Babysitters"],
        expected_by_season={
            1: set(range(1, 13)),
        },
        filename_patterns=[
            (
                r"^(?:Gakuen|Gamuen)\s+Babysitters\s+"
                r"S(?P<season>\d+)E(?P<start>\d+)$"
            ),
        ],
    ),

    "Hellsing": season_series(
        name="Hellsing",
        folder_names=["Hellsing"],
        expected_by_season={
            1: set(range(1, 14)),
        },
        keep_title=True,
    ),

    "Hoshifuru Oukoku no Nina": season_series(
        name="Hoshifuru Oukoku no Nina",
        folder_names=["Hoshifuru Oukoku no Nina"],
        expected_by_season={
            1: set(range(1, 13)),
        },
    ),

    "Hunter x Hunter": absolute_series(
        name="Hunter x Hunter",
        folder_names=[
            "Hunter x Hunter",
            "Hunter X Hunter",
            "Hunter × Hunter",
        ],
        total_episodes=148,
        seasons=[
            {"season": 1, "start": 1, "end": 148},
        ],
    ),

    "Ijiranaide Nagatoro-san": season_series(
        name="Ijiranaide Nagatoro-san",
        folder_names=[
            "Ijiranaide Nagatoro San",
            "Ijiranaide Nagatoro-san",
        ],
        expected_by_season={
            1: set(range(1, 13)),
            2: set(range(1, 13)),
        },
    ),

    "Kaguya-sama Love is War": season_series(
        name="Kaguya-sama Love is War",
        folder_names=["Kaguya-sama Love is War"],
        expected_by_season={
            1: set(range(1, 13)),
        },
        filename_patterns=[
            (
                r"^(?:Kaguya|Kagyua)\s+Sama.*?"
                r"S(?P<season>\d+)E(?P<start>\d+)$"
            ),
        ],
    ),

    "Karakai Jouzu no Takagi-san": season_series(
        name="Karakai Jouzu no Takagi-san",
        folder_names=["Karakai Jouzu no Takagi-San"],
        expected_by_season=None,
        note="Collection is currently incomplete.",
    ),

    "Kekkon Surutte Hontou Desu Ka": season_series(
        name="Kekkon Surutte Hontou Desu Ka",
        folder_names=["Kekkon Surutte Hontou Desu Ka"],
        expected_by_season={
            1: set(range(1, 13)),
        },
    ),

    "KonoSuba": season_series(
        name="KonoSuba",
        folder_names=[
            "KonoSuba",
            "KonoSuba Gods Blessing on This Wonderful World",
        ],
        expected_by_season={
            1: set(range(1, 11)),
            2: set(range(1, 11)),
            3: set(range(1, 13)),
        },
    ),

    "Nagasarete Airantou": season_series(
        name="Nagasarete Airantou",
        folder_names=["Nagasarete Airantou"],
        expected_by_season=None,
        note="Collection is currently incomplete.",
    ),

    "Neon Genesis Evangelion": season_series(
        name="Neon Genesis Evangelion",
        folder_names=["Neon Genesis Evangelion"],
        expected_by_season={
            1: set(range(1, 27)),
        },
    ),

    "One Punch Man": season_series(
        name="One Punch Man",
        folder_names=["One Punch Man"],
        expected_by_season={
            1: set(range(1, 13)),
        },
    ),
        "Oniichan wa Oshima": season_series(
        name="Oniichan wa Oshima",
        folder_names=[
            "Oniichan wa Oshima",
        ],
        expected_by_season={
            1: set(range(1, 13)),
        },
    ),

    "Sakura Card Captor": season_series(
        name="Sakura Card Captor",
        folder_names=[
            "Sakura Card Captor",
            "Cardcaptor Sakura",
        ],
        expected_by_season={
            1: set(range(1, 71)),
        },
    ),

    "Samurai Champloo": season_series(
        name="Samurai Champloo",
        folder_names=[
            "Samurai Champloo",
        ],
        expected_by_season={
            1: set(range(1, 25)),
        },
    ),

    "Seishun Buta Yarou wa Bunny Girl Senpai no Yume wo Minai":
        season_series(
            name=(
                "Seishun Buta Yarou wa "
                "Bunny Girl Senpai no Yume wo Minai"
            ),
            folder_names=[
                (
                    "Seishun Buta Yarou wa "
                    "Bunny Girl Senpai no Yume wo Minai"
                ),
            ],

            # Não definimos um total esperado por enquanto.
            # A pasta contém somente E01, E02 e E04.
            expected_by_season=None,

            note=(
                "Current collection contains "
                "S01E01, S01E02 and S01E04."
            ),
        ),

    "Tatte no Yuusha no Nariagari": season_series(
        name="Tatte no Yuusha no Nariagari",
        folder_names=[
            "Tatte no Yuusha no Nariagari",
        ],
        expected_by_season={
            1: set(range(1, 26)),
            2: set(range(1, 14)),
            3: set(range(1, 13)),
            4: set(range(1, 13)),
        },
    ),

    "Trigun": season_series(
        name="Trigun",
        folder_names=[
            "Trigun",
        ],
        expected_by_season={
            1: set(range(1, 27)),
        },

        # Trigun usa "Trigun Dublado 01",
        # sem S01E01 no nome original.
        filename_patterns=[
            (
                r"^Trigun\s+Dublado\s+"
                r"(?P<start>\d{1,2})$"
            ),
        ],
    ),

    "Tsurezure Children": season_series(
        name="Tsurezure Children",
        folder_names=[
            "Tsurezure Children",
        ],
        expected_by_season={
            1: set(range(1, 13)),
        },
    ),
}