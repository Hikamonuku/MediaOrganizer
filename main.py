from organizer import organize_series
from scanner import scan_library

from Media.anime import ANIME
from Media.cartoons import CARTOONS
from Media.movies import MOVIES
from Media.tv_series import TV_SERIES


def build_menu(
    media_database: dict,
) -> dict[str, dict]:
    menu_options = {}

    sorted_media = sorted(
        media_database.values(),
        key=lambda item: item["name"].casefold(),
    )

    for index, media_data in enumerate(
        sorted_media,
        start=1,
    ):
        option = str(index)
        menu_options[option] = media_data

        marker = (
            ""
            if media_data.get("enabled", True)
            else " [manual review]"
        )

        print(
            f"{option}. "
            f"{media_data['name']}"
            f"{marker}"
        )

    print("0. Back")

    return menu_options


def organize_one(
    media_database: dict,
    title: str,
) -> None:
    while True:
        print(f"\n==== {title} Organizer ====")

        menu_options = build_menu(
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

        path = input(
            f"\n{media_data['name']} folder: "
        )

        organize_series(
            path=path,
            series_data=media_data,
        )


def scan_media_library(
    media_database: dict,
    library_name: str,
) -> None:
    path = input(
        f"\n{library_name} folder: "
    )

    scan_library(
        path=path,
        media_database=media_database,
        library_name=library_name,
    )


def main() -> None:
    while True:
        print("\n==== Media Organizer ====")
        print("1. Anime")
        print("2. Cartoons")
        print("3. TV series")
        print("4. Movies")
        print("5. Scan anime library")
        print("6. Scan cartoon library")
        print("7. Exit")

        option = input(
            "\nSelect an option: "
        ).strip()

        if option == "1":
            organize_one(
                media_database=ANIME,
                title="Anime",
            )

        elif option == "2":
            organize_one(
                media_database=CARTOONS,
                title="Cartoon",
            )

        elif option == "3":
            organize_one(
                media_database=TV_SERIES,
                title="TV Series",
            )

        elif option == "4":
            print(
                "\nMovie organization "
                "is not implemented yet."
            )

        elif option == "5":
            scan_media_library(
                media_database=ANIME,
                library_name="Anime library",
            )

        elif option == "6":
            scan_media_library(
                media_database=CARTOONS,
                library_name="Cartoon library",
            )

        elif option == "7":
            print(
                "\nClosing Media Organizer..."
            )
            break

        else:
            print("\nInvalid option.")


if __name__ == "__main__":
    main()