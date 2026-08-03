from database import season_series


CARTOONS = {
    "Avatar: The Last Airbender": season_series(
        name="Avatar The Last Airbender",
        folder_names=[
            "Avatar The Last Airbender",
            "Avatar: The Last Airbender",
        ],
        expected_by_season={
            1: set(range(1, 21)),
            2: set(range(1, 21)),
            3: set(range(1, 22)),
        },
        keep_title=True,
    ),

    "Caverna do Dragão": season_series(
        name="Caverna do Dragão",
        folder_names=[
            "Caverna do Dragão",
        ],
        expected_by_season=None,
        keep_title=True,
        enabled=False,
        note=(
            "Episode numbering after S01E15 "
            "needs manual correction."
        ),
    ),

    "Duck Dodgers": season_series(
        name="Duck Dodgers",
        folder_names=[
            "Duck Dodgers",
        ],
        expected_by_season={
            1: set(range(1, 14)),
        },
        keep_title=True,
        filename_patterns=[
            (
                r"^Duck\.Dodgers\."
                r"S(?P<season>\d{1,2})"
                r"E(?P<start>\d{1,3})"
                r"(?:\s*-\s*(?P<title>.+))?$"
            ),
        ],
    ),
}