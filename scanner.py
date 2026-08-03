import re
from pathlib import Path


def normalize_name(name: str) -> str:
    normalized = name.casefold()
    normalized = normalized.replace("×", "x")
    normalized = re.sub(r"\([^)]*\)", "", normalized)
    normalized = re.sub(r"[-_.:]", " ", normalized)
    normalized = re.sub(r"\s+", " ", normalized)

    return normalized.strip()


def find_media_by_folder(
    folder_name: str,
    media_database: dict,
) -> dict | None:
    normalized_folder = normalize_name(folder_name)

    for media_data in media_database.values():
        aliases = media_data.get(
            "folder_names",
            [media_data["name"]],
        )

        for alias in aliases:
            if normalize_name(alias) == normalized_folder:
                return media_data

    return None


def scan_library(
    path: str,
    media_database: dict,
    library_name: str,
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

    folders = sorted(
        [
            item
            for item in library_folder.iterdir()
            if item.is_dir()
        ],
        key=lambda item: item.name.casefold(),
    )

    for media_folder in folders:
        media_data = find_media_by_folder(
            folder_name=media_folder.name,
            media_database=media_database,
        )

        if media_data is None:
            unsupported.append(media_folder)
            continue

        item = {
            "folder": media_folder,
            "media": media_data,
        }

        if media_data.get("enabled", True):
            supported.append(item)
        else:
            disabled.append(item)

    print(f"\n==== {library_name} Report ====\n")

    print("Supported:")

    for item in supported:
        print(
            f"  [OK] {item['folder'].name}"
            f" -> {item['media']['name']}"
        )

    print("\nManual review / disabled:")

    for item in disabled:
        print(
            f"  [!!] {item['folder'].name}"
            f" -> {item['media'].get('note', 'Disabled')}"
        )

    print("\nNot registered:")

    for folder in unsupported:
        print(f"  [--] {folder.name}")

    print("\n==== Summary ====")
    print(f"Folders found: {len(folders)}")
    print(f"Supported: {len(supported)}")
    print(f"Disabled: {len(disabled)}")
    print(f"Not registered: {len(unsupported)}")

    return {
        "library_folder": library_folder,
        "supported": supported,
        "disabled": disabled,
        "unsupported": unsupported,
    }