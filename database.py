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
    # Exemplo:
    # Death Note - S01E01 - Rebirth
    # Dr. Stone S01E01
    # Kekkon Surutte Hontou Desu Ka S1E1
    "season_episode": (
        r"^.*?"
        r"S(?P<season>\d{1,2})"
        r"E(?P<start>\d{1,3})"
        r"(?:[-_](?:E)?(?P<end>\d{1,3}))?"
        r"(?:\s*-\s*(?P<title>.+))?$"
    ),

    # Exemplo:
    # Hunter X Hunter 001
    # Ergo Proxy 023
    "absolute_episode": (
        r"^.*?\s+(?P<start>\d{1,3})$"
    ),

    # Formato antigo do Dragon Ball Z.
    "dbz_old": (
        r"^DBZ_Episodio\s+"
        r"(?P<start>\d{3})"
    ),

    # Formato já organizado do Dragon Ball Z.
    "dbz_organized": (
        r"^Dragon Ball Z\s*-\s*"
        r"S(?P<season>\d{1,2})"
        r"E(?P<season_episode>\d{1,3})"
        r"\s*-\s*(?P<start>\d{3})"
    ),

    # Padrões antigos encontrados em Bleach.
    "bleach_epi": (
        r"^.*?Epi[_\s.-]*"
        r"(?P<start>\d{1,3})"
        r"(?:[_-](?P<end>\d{1,3}))?$"
    ),

    "bleach_simple": (
        r"^Bleach\s*-\s*"
        r"(?P<start>\d{1,3})$"
    ),
}