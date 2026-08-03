from organizer import organize_series
from scanner import scan_library

from Media.anime import ANIME
from Media.cartoons import CARTOONS
from Media.tv_series import TV_SERIES
from Media.movies import MOVIES
from Core.audiobook_scanner import (
    scan_audiobook_library,
)

MEDIA_TYPES = {
    "1": ("Anime", ANIME),
    "2": ("Cartoons", CARTOONS),
    "3": ("TV Series", TV_SERIES),
    "4": ("Movies", MOVIES),
}

def show_media_menu() -> None:
    print("\n==== Media Organizer ====")
    print("1. Anime")
    print("2. Cartoons")
    print("3. TV Series")
    print("4. Movies")
    print("5. Audio")
    print("0. Exit")

def show_library_menu(media_name: str) -> None:
    print(f"\n==== {media_name} ====")
    print("1. Organize one")
    print("2. Scan library")
    print("3. Organize library")
    print("0. Back")


def organize_one(media_name: str, media_database: dict) -> None:
    print(f"\n==== {media_name} ====\n")

    options = list(media_database.items())

    for index, (_, media) in enumerate(options, start=1):
        print(f"{index}. {media['name']}")

    print("0. Back")

    option = input("\nSelect: ").strip()

    if option == "0":
        return

    try:
        selected = options[int(option) - 1][1]
    except (ValueError, IndexError):
        print("\nInvalid option.")
        return

    folder = input(
        f"\n{selected['name']} folder: "
    )

    organize_series(
        path=folder,
        series_data=selected,
    )


def media_menu(
    media_name: str,
    media_database: dict,
) -> None:

    while True:

        show_library_menu(media_name)

        option = input(
            "\nSelect an option: "
        ).strip()

        if option == "0":
            return

        elif option == "1":
            organize_one(
                media_name,
                media_database,
            )

        elif option == "2":
            folder = input(
                f"\n{media_name} library: "
            )

            scan_library(
                folder,
                media_database,
            )

        elif option == "3":
            print(
                "\nLibrary organizer "
                "is not implemented yet."
            )

        else:
            print("\nInvalid option.")

def main() -> None:
    while True:
        show_media_menu()
        option = input(
            "\nSelect a category: "
        ).strip()
        if option == "0":
            print(
                "\nClosing Media Organizer..."
            )
            break
        if option == "5":
            audio_menu()
            continue
        selected = MEDIA_TYPES.get(option)
        if selected is None:
            print("\nInvalid option.")
            continue
        media_name, media_database = selected
        media_menu(
            media_name,
            media_database,
        )

def audio_menu() -> None:
    while True:
        print("\n==== Audio ====")
        print("1. Scan entire audio library")
        print("2. Scan audiobooks")
        print("3. Music")
        print("4. Podcasts")
        print("5. Courses")
        print("0. Back")

        option = input(
            "\nSelect an option: "
        ).strip()

        if option == "0":
            return

        if option == "1":
            path = input(
                "\nAudio library folder: "
            )

            scan_audio_library(path)

        elif option == "2":
            path = input(
                "\nAudiobooks folder: "
            )

            scan_audiobook_library(path)

        elif option in {"3", "4", "5"}:
            print(
                "\nThis audio module "
                "is not implemented yet."
            )

        else:
            print("\nInvalid option.")

if __name__ == "__main__":
    main()