from database import season_series


TV_SERIES = {
    "90 Day Fiancé The Other Way": season_series(
        name="90 Day Fiancé The Other Way",
        folder_names=[
            "90 Day Fiancé The Other Way",
            "90 Day Fiance The Other Way",
        ],
        expected_by_season=None,
        keep_title=True,
        note=(
            "Current collection contains only "
            "S01E00 about Paul and Karine."
        ),
    ),

    "A Catedral do Mar": season_series(
        name="A Catedral do Mar",
        folder_names=[
            "Catedral do Mar",
            "A Catedral do Mar",
        ],
        expected_by_season={
            1: set(range(1, 9)),
        },
        filename_patterns=[
            (
                r"^A\.Catedral\.do\.Mar\."
                r"S(?P<season>\d{1,2})"
                r"E(?P<start>\d{1,3})"
                r".*$"
            ),
        ],
    ),

    "Chaves": season_series(
        name="Chaves",
        folder_names=[
            "Chaves",
        ],
        expected_by_season=None,
        keep_title=True,
        enabled=False,
        note=(
            "Collection contains unnumbered S00E files, "
            "missing episode numbers and duplicate S01E269."
        ),
    ),

    "Dr. House": season_series(
        name="Dr. House",
        folder_names=[
            "Dr. House",
            "House",
            "House M.D.",
        ],
        expected_by_season={
            3: set(range(1, 25)),
            4: set(range(1, 17)),
        },
        keep_title=True,
        filename_patterns=[
            (
                r"^House\s+"
                r"S(?P<season>\d{1,2})"
                r"E(?P<start>\d{1,2})"
                r"(?:\s*-\s*(?P<title>.+))?$"
            ),
        ],
        note=(
            "The current folder contains only Seasons 3 and 4 "
            "and may have missing episodes."
        ),
    ),

    "Duas Garotas em Apuros": season_series(
        name="Duas Garotas em Apuros",
        folder_names=[
            "Duas Garotas em Apuros",
            "2 Broke Girls",
        ],
        expected_by_season={
            1: set(range(1, 25)),
            2: set(range(1, 25)),
            3: set(range(1, 25)),
            4: set(range(1, 23)),
        },
        keep_title=True,
        filename_patterns=[
            # S01E01 - Pilot
            (
                r"^"
                r"S(?P<season>1)"
                r"E(?P<start>\d{1,2})"
                r"(?:\s*-\s*(?P<title>.+))?$"
            ),

            # 2 Broke Girls S02E01 - ...
            (
                r"^2\s+Broke\s+Girls\s+"
                r"S(?P<season>[23])"
                r"E(?P<start>\d{1,2})"
                r"(?:\s*-\s*(?P<title>.+?))?"
                r"(?:\s+720p.*)?$"
            ),

            # 2.Garotas.Apuros.04.01...
            (
                r"^2\.Garotas\.Apuros\."
                r"(?P<season>04)\."
                r"(?P<start>\d{2})"
                r".*$"
            ),
        ],
    ),

    "Família Dinossauros": season_series(
        name="Família Dinossauros",
        folder_names=[
            "Família Dinossauros",
            "Família Dinossauro",
        ],
        expected_by_season={
            1: set(range(1, 66)),
        },
        keep_title=True,
        filename_patterns=[
            (
                r"^Família\s+Dinossauros\s+"
                r"S(?P<season>\d{1,2})"
                r"E(?P<start>\d{1,3})"
                r"(?:\s*[-.]\s*(?P<title>.+))?$"
            ),
        ],
    ),

    "iCarly": season_series(
        name="iCarly",
        folder_names=[
            "iCarly",
        ],
        expected_by_season={
            1: set(range(1, 26)),
            2: set(range(1, 22)),
            3: set(range(1, 19)),
            4: set(range(1, 11)),
            5: set(range(1, 11)),
        },
        keep_title=True,
    ),

    "Kenan e Kel": season_series(
        name="Kenan e Kel",
        folder_names=[
            "Kenan e Kel",
        ],
        expected_by_season={
            1: set(range(1, 15)),
            2: set(range(1, 14)),
            3: set(range(1, 23)),
            4: set(range(1, 14)),
        },
        keep_title=True,
        note=(
            "The scanner should report missing episodes "
            "in Seasons 3 and 4."
        ),
    ),

    "Pesadelo na Cozinha": season_series(
        name="Pesadelo na Cozinha",
        folder_names=[
            "Pesadelo na Cozinha",
        ],
        expected_by_season=None,
        keep_title=True,
        note=(
            "Current collection contains only "
            "S02E01 - Pé de Fava."
        ),
    ),

    "Prepare-Se": season_series(
        name="Prepare-Se",
        folder_names=[
            "Prepare-Se",
            "Prepare-se",
        ],
        expected_by_season={
            1: set(range(1, 51)),
        },
        keep_title=True,
        filename_patterns=[
            (
                r"^Prepare-se\s+"
                r"S(?P<season>\d{1,2})"
                r"E(?P<start>\d{1,3})"
                r"(?:\s+\(Completo\))?"
                r"(?:\s*-\s*(?P<title>.+))?$"
            ),
        ],
        note=(
            "Independent DVD series by Rubens Sodré."
        ),
    ),

    "Ragnarok": season_series(
        name="Ragnarok",
        folder_names=[
            "Ragnarok",
        ],
        expected_by_season={
            2: set(range(1, 7)),
            3: set(range(1, 7)),
        },
        note=(
            "Current collection contains Seasons 2 and 3 only."
        ),
    ),

    "Sherlock": season_series(
        name="Sherlock",
        folder_names=[
            "Sherlock",
            "Sherlock Holmes",
        ],
        expected_by_season=None,
        keep_title=True,
        enabled=False,
        note=(
            "The files do not match the normal three-episode "
            "season structure and need manual identification."
        ),
    ),

    "The Big Bang Theory": season_series(
        name="The Big Bang Theory",
        folder_names=[
            "The Big Bang Theory",
        ],
        expected_by_season={
            1: set(range(1, 18)),
        },
        keep_title=True,
        note=(
            "Current collection contains Season 1 only."
        ),
    ),

    "The Office (US)": season_series(
        name="The Office (US)",
        folder_names=[
            "The Office (US)",
            "The Office US",
        ],
        expected_by_season={
            1: set(range(1, 7)),
            2: set(range(1, 23)),
            3: set(range(1, 26)),
            4: set(range(1, 15)),
            5: set(range(1, 29)),
            6: set(range(1, 27)),
            7: set(range(1, 27)),
            8: set(range(1, 25)),
            9: set(range(1, 28)),
        },
        filename_patterns=[
            (
                r"^The\.Office\."
                r"S(?P<season>\d{1,2})"
                r"E(?P<start>\d{1,3})"
                r".*$"
            ),
        ],
    ),

    "Um Maluco no Pedaço": season_series(
        name="Um Maluco no Pedaço",
        folder_names=[
            "Um Maluco No Pedaço",
            "Um Maluco no Pedaço",
        ],
        expected_by_season=None,
        keep_title=True,
        filename_patterns=[
            (
                r"^Um\s+Maluco\s+no\s+Pedaço\s+"
                r"S(?P<season>\d{1,2})"
                r"E(?P<start>\d{1,2})"
                r"(?:\s*-\s*(?P<title>.+))?$"
            ),
        ],
        note=(
            "Current collection contains only parts "
            "of Seasons 1, 2, 5 and 6."
        ),
    ),
}