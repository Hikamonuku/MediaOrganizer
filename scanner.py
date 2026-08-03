from pathlib import Path
import re

def normalize_name(name: str) -> str:
    name = name.lower()
    name = name.replace("×", "x")
    # remove tudo entre parênteses
    name = re.sub(r"\(.*?\)", "", name)
    # troca separadores por espaço
    name = re.sub(r"[-_]", " ", name)
    # remove espaços duplicados
    name = re.sub(r"\s+", " ", name)
    return name.strip()

def find_series_by_folder(
    folder_name: str,
    series_database: dict,
) -> dict | None:
    normalized_folder = normalize_name(folder_name)
    for series_data in series_database.values():
        folder_names = series_data.get(
            "folder_names",
            [series_data["name"]],
        )
        for registered_name in folder_names:
            if normalize_name(registered_name) == normalized_folder:
                return series_data
    return None


def scan_anime_library(
    path: str,
    series_database: dict,
) -> None:
    library_folder = Path(
        path.strip().strip('"')
    )

    if not library_folder.exists():
        print("\nLibrary folder not found.")
        return

    if not library_folder.is_dir():
        print("\nThe provided path is not a folder.")
        return
    supported = []
    unsupported = []
    folders = sorted(
        [
            item
            for item in library_folder.iterdir()
            if item.is_dir()
        ],
        key=lambda folder: folder.name.lower(),
    )
    for anime_folder in folders:
        series_data = find_series_by_folder(
            folder_name=anime_folder.name,
            series_database=series_database,
        )
        if series_data is None:
            unsupported.append(anime_folder.name)
        else:
            supported.append(
                {
                    "folder": anime_folder,
                    "series": series_data,
                }
            )
    print("\n==== Anime Library Report ====\n")
    print("Supported anime:")
    if supported:
        for item in supported:
            print(
                f"  [OK] {item['folder'].name}"
                f" -> {item['series']['name']}"
            )
    else:
        print("  None")
    print("\nNot registered:")
    if unsupported:
        for folder_name in unsupported:
            print(f"  [--] {folder_name}")
    else:
        print("  None")
    print("\n==== Summary ====")
    print(f"Folders found: {len(folders)}")
    print(f"Supported: {len(supported)}")
    print(f"Not registered: {len(unsupported)}")