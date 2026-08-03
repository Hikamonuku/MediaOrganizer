from database import (
    FILENAME_PATTERNS,
    absolute_series,
    season_series,
)


ANIME = {
    "Another": season_series(
        name="Another",
        folder_names=["Another"],
        expected_by_season={
            0: {1},
            1: set(range(1, 13)),
        },
        keep_title=True,
    ),

    # Restante dos animes...
}