import re
from pathlib import Path


def normalize_name(name: str) -> str:
    normalized = name.casefold()
    normalized = normalized.replace("×", "x")

    # Remove anos e outros textos entre parênteses.
    normalized = re.sub(r"\([^)]*\)", "", normalized)

    # Troca separadores por espaço.
    normalized = re.sub(r"[-_.]", " ", normalized)

    # Remove espaços repetidos.
    normalized = re.sub(r"\s+", " ", normalized)

    return normalized.strip()


def find_series_by_folder(
    folder_name: str,
    series_database: dict,
) -> dict | None:
    normalized_folder = normalize_name(folder_name)

    for series_data in series_database.values():
        aliases = series_data.get(
            "folder_names",
            [series_data["name"]],
        )

        for alias in aliases:
            if normalize_name(alias) == normalized_folder:
                return series_data

    return None


def get_anime_folders(library_folder: Path) -> list[Path]:
    return sorted(
        [
            item
            for item in library_folder.iterdir()
            if item.is_dir()
        ],
        key=lambda item: item.name.casefold(),
    )


def scan_anime_library(
    path: str,
    series_database: dict,
) -> dict | None:
    library_folder = Path(
        path.strip().strip('"')
    )

    if not library_folder.exists():
        print("\nLibrary folder not found.")
        return None

    if not library_folder.is_dir():
        print("\nThe provided path is not a folder.")
        return None

    supported = []
    disabled = []
    unsupported = []

    for anime_folder in get_anime_folders(library_folder):
        series_data = find_series_by_folder(
            folder_name=anime_folder.name,
            series_database=series_database,
        )

        if series_data is None:
            unsupported.append(anime_folder)
            continue

        item = {
            "folder": anime_folder,
            "series": series_data,
        }

        if series_data.get("enabled", True):
            supported.append(item)
        else:
            disabled.append(item)

    print("\n==== Anime Library Report ====\n")

    print("Supported:")

    if supported:
        for item in supported:
            print(
                f"  [OK] {item['folder'].name}"
                f" -> {item['series']['name']}"
            )
    else:
        print("  None")

    print("\nManual review / disabled:")

    if disabled:
        for item in disabled:
            note = item["series"].get("note", "")

            print(
                f"  [!!] {item['folder'].name}"
                f" -> {note or 'Disabled'}"
            )
    else:
        print("  None")

    print("\nNot registered:")

    if unsupported:
        for folder in unsupported:
            print(f"  [--] {folder.name}")
    else:
        print("  None")

    print("\n==== Summary ====")
    print(
        f"Folders found: "
        f"{len(supported) + len(disabled) + len(unsupported)}"
    )
    print(f"Supported: {len(supported)}")
    print(f"Disabled: {len(disabled)}")
    print(f"Not registered: {len(unsupported)}")

    return {
        "library_folder": library_folder,
        "supported": supported,
        "disabled": disabled,
        "unsupported": unsupported,
    }