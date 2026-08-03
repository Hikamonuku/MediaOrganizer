from Core.audio_scanner import scan_audio_library
from Core.audiobook_scanner import scan_audiobook_library

from organizer import organize_series
from scanner import scan_library

from Media.anime import ANIME
from Media.cartoons import CARTOONS
from Media.movies import MOVIES
from Media.tv_series import TV_SERIES

MEDIA_TYPES = {
    "1": {
        "name": "Anime",
        "library_name": "Anime Library",
        "database": ANIME,
    },
    "2": {
        "name": "Cartoons",
        "library_name": "Cartoon Library",
        "database": CARTOONS,
    },
    "3": {
        "name": "TV Series",
        "library_name": "TV Series Library",
        "database": TV_SERIES,
    },
    "4": {
        "name": "Movies",
        "library_name": "Movie Library",
        "database": MOVIES,
    },
}

def build_media_item_menu(
    media_database: dict,
) -> dict[str, dict]:
    """
    Cria automaticamente o menu de itens
    em ordem alfabética.
    """
    menu_options = {}

    sorted_items = sorted(
        media_database.values(),
        key=lambda item: item["name"].casefold(),
    )

    for index, media_data in enumerate(
        sorted_items,
        start=1,
    ):
        option = str(index)
        menu_options[option] = media_data

        marker = ""

        if not media_data.get("enabled", True):
            marker = " [manual review]"

        print(
            f"{option}. "
            f"{media_data['name']}"
            f"{marker}"
        )

    print("0. Back")

    return menu_options


def organize_one_media(
    media_name: str,
    media_database: dict,
) -> None:
    """
    Permite escolher e organizar apenas
    uma série, anime, desenho ou filme.
    """
    if not media_database:
        print(
            f"\nThe {media_name.lower()} "
            "database is empty."
        )
        return

    while True:
        print(
            f"\n==== Organize One "
            f"{media_name} ===="
        )

        menu_options = build_media_item_menu(
            media_database
        )

        option = input(
            "\nSelect an item: "
        ).strip()

        if option == "0":
            return

        media_data = menu_options.get(option)

        if media_data is None:
            print("\nInvalid option.")
            continue

        folder = input(
            f"\n{media_data['name']} folder: "
        )

        organize_series(
            path=folder,
            series_data=media_data,
        )


def organize_media_library(
    scan_result: dict,
) -> None:
    """
    Organiza todos os itens habilitados
    encontrados pelo scanner.
    """
    supported = scan_result["supported"]

    if not supported:
        print(
            "\nNo supported and enabled "
            "items were found."
        )
        return

    print(
        "\nOnly supported and enabled "
        "items will be organized."
    )

    if scan_result["disabled"]:
        print(
            "Items marked for manual review "
            "will be skipped."
        )

    if scan_result["unsupported"]:
        print(
            "Unregistered folders "
            "will be skipped."
        )

    confirmation = input(
        "\nOrganize all supported items? "
        "(yes/no): "
    ).strip().lower()

    if confirmation not in {"yes", "y"}:
        print("\nOperation cancelled.")
        return

    results = []

    for item in supported:
        media_folder = item["folder"]
        media_data = item["media"]

        print("\n" + "=" * 60)
        print(media_data["name"])
        print("=" * 60)

        result = organize_series(
            path=str(media_folder),
            series_data=media_data,
            ask_confirmation=False,
        )

        results.append(
            {
                "name": media_data["name"],
                "result": result,
            }
        )

    print(
        "\n==== Library Organization "
        "Result ====\n"
    )

    for item in results:
        result = item["result"]

        status = result.get(
            "status",
            "unknown",
        )

        moved = result.get(
            "moved",
            0,
        )

        skipped = result.get(
            "skipped",
            0,
        )

        print(
            f"{item['name']}: "
            f"{status} | "
            f"moved: {moved} | "
            f"skipped: {skipped}"
        )


def media_library_menu(
    media_database: dict,
    library_name: str,
) -> None:
    """
    Submenu para analisar ou organizar
    uma biblioteca inteira.
    """
    if not media_database:
        print(
            f"\nThe {library_name.lower()} "
            "database is empty."
        )
        return

    while True:
        print(
            f"\n==== {library_name} ===="
        )
        print("1. Scan library")
        print("2. Scan and organize library")
        print("0. Back")

        option = input(
            "\nSelect an option: "
        ).strip()

        if option == "0":
            return

        if option not in {"1", "2"}:
            print("\nInvalid option.")
            continue

        folder = input(
            f"\n{library_name} folder: "
        )

        scan_result = scan_library(
            path=folder,
            media_database=media_database,
            library_name=library_name,
        )

        if scan_result is None:
            continue

        if option == "2":
            organize_media_library(
                scan_result=scan_result,
            )


def video_category_menu(
    media_name: str,
    library_name: str,
    media_database: dict,
) -> None:
    """
    Menu de uma categoria de vídeo,
    como Anime ou TV Series.
    """
    while True:
        print(f"\n==== {media_name} ====")
        print(f"1. Organize one {media_name.lower()}")
        print(f"2. {library_name}")
        print("0. Back")

        option = input(
            "\nSelect an option: "
        ).strip()

        if option == "0":
            return

        if option == "1":
            organize_one_media(
                media_name=media_name,
                media_database=media_database,
            )

        elif option == "2":
            media_library_menu(
                media_database=media_database,
                library_name=library_name,
            )

        else:
            print("\nInvalid option.")


def video_menu() -> None:
    """
    Menu principal das mídias de vídeo.
    """
    while True:
        print("\n==== Video ====")
        print("1. Anime")
        print("2. Cartoons")
        print("3. TV Series")
        print("4. Movies")
        print("0. Back")
        option = input(
            "\nSelect a video category: "
        ).strip()
        if option == "0":
            return
        selected = MEDIA_TYPES.get(option)
        if selected is None:
            print("\nInvalid option.")
            continue
        video_category_menu(
            media_name=selected["name"],
            library_name=selected["library_name"],
            media_database=selected["database"],
        )

def audio_menu() -> None:
    """
    Menu principal das mídias de áudio.
    """
    while True:
        print("\n==== Audio ====")
        print("1. Scan entire audio library")
        print("2. Scan audiobooks")
        print("3. Music")
        print("4. Podcasts")
        print("5. Courses")
        print("6. Lectures")
        print("0. Back")

        option = input(
            "\nSelect an option: "
        ).strip()

        if option == "0":
            return

        if option == "1":
            folder = input(
                "\nAudio library folder: "
            )

            scan_audio_library(folder)

        elif option == "2":
            folder = input(
                "\nAudiobooks folder: "
            )

            scan_audiobook_library(folder)

        elif option == "3":
            print(
                "\nMusic organization "
                "is not implemented yet."
            )

        elif option == "4":
            print(
                "\nPodcast organization "
                "is not implemented yet."
            )

        elif option == "5":
            print(
                "\nCourse organization "
                "is not implemented yet."
            )

        elif option == "6":
            print(
                "\nLecture organization "
                "is not implemented yet."
            )

        else:
            print("\nInvalid option.")


def main() -> None:
    while True:
        print("\n==== Media Organizer ====")
        print("1. Video")
        print("2. Audio")
        print("3. Settings")
        print("0. Exit")

        option = input(
            "\nSelect a media type: "
        ).strip()

        if option == "0":
            print(
                "\nClosing Media Organizer..."
            )
            break

        if option == "1":
            video_menu()

        elif option == "2":
            audio_menu()

        elif option == "3":
            print(
                "\nSettings are not "
                "implemented yet."
            )

        else:
            print("\nInvalid option.")


if __name__ == "__main__":
    main()