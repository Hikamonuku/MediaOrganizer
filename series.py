SERIES = {

    "Dragon Ball": {
        "episodes": 153,
        "folder": "Season 01",
        "pattern":
        r"Dragon Ball S1E(\d{3}) - (.+)"
    },
    "Dragon Ball Z": {
        "episodes": 291,
        "seasons": [
            (1,1,39),
            (2,40,74),
            ...
            (9,254,291)
        ],
        "pattern":
        r"DBZ_Episodio (\d{3})"
    }
}