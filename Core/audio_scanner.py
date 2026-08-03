from collections import Counter
from pathlib import Path


AUDIO_EXTENSIONS = {
    ".mp3",
    ".wav",
    ".flac",
    ".m4a",
    ".aac",
    ".ogg",
    ".opus",
    ".wma",
    ".mid",
    ".midi",
}


def prepare_audio_folder(path: str) -> Path | None:
    folder = Path(path.strip().strip('"'))

    if not folder.exists():
        print("\nAudio library not found.")
        return None

    if not folder.is_dir():
        print("\nThe provided path is not a folder.")
        return None

    return folder


def scan_audio_category(folder: Path) -> dict:
    audio_files = [
        file_path
        for file_path in folder.rglob("*")
        if (
            file_path.is_file()
            and file_path.suffix.lower()
            in AUDIO_EXTENSIONS
        )
    ]

    direct_subfolders = [
        item
        for item in folder.iterdir()
        if item.is_dir()
    ]

    loose_audio_files = [
        file_path
        for file_path in folder.iterdir()
        if (
            file_path.is_file()
            and file_path.suffix.lower()
            in AUDIO_EXTENSIONS
        )
    ]

    extensions = Counter(
        file_path.suffix.lower()
        for file_path in audio_files
    )

    return {
        "folder": folder,
        "subfolders": len(direct_subfolders),
        "audio_files": len(audio_files),
        "loose_audio_files": len(loose_audio_files),
        "extensions": dict(
            sorted(extensions.items())
        ),
    }


def scan_audio_library(path: str) -> dict | None:
    library = prepare_audio_folder(path)

    if library is None:
        return None

    category_folders = sorted(
        [
            item
            for item in library.iterdir()
            if item.is_dir()
        ],
        key=lambda item: item.name.casefold(),
    )

    categories = [
        scan_audio_category(folder)
        for folder in category_folders
    ]

    print("\n==== Audio Library Report ====\n")

    total_files = 0

    for category in categories:
        total_files += category["audio_files"]

        print(category["folder"].name)
        print(
            f"  Subfolders: "
            f"{category['subfolders']}"
        )
        print(
            f"  Audio files: "
            f"{category['audio_files']}"
        )
        print(
            "  Loose audio files: "
            f"{category['loose_audio_files']}"
        )

        if category["extensions"]:
            extension_text = ", ".join(
                f"{extension}: {amount}"
                for extension, amount
                in category["extensions"].items()
            )

            print(f"  Formats: {extension_text}")

        print()

    print("==== Summary ====")
    print(f"Categories: {len(categories)}")
    print(f"Audio files: {total_files}")

    return {
        "library": library,
        "categories": categories,
        "total_files": total_files,
    }