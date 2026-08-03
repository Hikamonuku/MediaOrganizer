from organizer import organize_series
from scanner import scan_library

from Media.anime import ANIME
from Media.cartoons import CARTOONS
from Media.movies import MOVIES
from Media.tv_series import TV_SERIES


def build_media_menu(
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


def organize_one_item(
    media_database: dict,
    media_type: str,
) -> None:
    if not media_database:
        print(
            f"\nThe {media_type.lower()} "
            "database is empty."
        )
        return

    while True:
        print(
            f"\n==== Organize One "
            f"{media_type} ===="
        )

        menu_options = build_media_menu(
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


def organize_library(
    scan_result: dict,
) -> None:
    supported = scan_result["supported"]

    if not supported:
        print(
            "\nNo supported and enabled "
            "items were found."
        )
        return

    print(
        "\nOnly supported and enabled items "
        "will be organized."
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

        print("\n" + "=" * 50)
        print(media_data["name"])
        print("=" * 50)

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


def library_menu(
    media_database: dict,
    library_name: str,
) -> None:
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

        path = input(
            f"\n{library_name} folder: "
        )

        scan_result = scan_library(
            path=path,
            media_database=media_database,
            library_name=library_name,
        )

        if scan_result is None:
            continue

        if option == "2":
            organize_library(
                scan_result=scan_result,
            )


def media_type_menu(
    media_database: dict,
    media_type: str,
    library_name: str,
) -> None:
    while True:
        print(
            f"\n==== {media_type} ===="
        )
        print(
            f"1. Organize one "
            f"{media_type.lower()}"
        )
        print(
            f"2. {library_name}"
        )
        print("0. Back")

        option = input(
            "\nSelect an option: "
        ).strip()

        if option == "0":
            return

        if option == "1":
            organize_one_item(
                media_database=media_database,
                media_type=media_type,
            )

        elif option == "2":
            library_menu(
                media_database=media_database,
                library_name=library_name,
            )

        else:
            print("\nInvalid option.")


def main() -> None:
    while True:
        print("\n==== Media Organizer ====")
        print("1. Anime")
        print("2. Cartoons")
        print("3. TV Series")
        print("4. Movies")
        print("5. Exit")

        option = input(
            "\nSelect a media type: "
        ).strip()

        if option == "1":
            media_type_menu(
                media_database=ANIME,
                media_type="Anime",
                library_name="Anime Library",
            )

        elif option == "2":
            media_type_menu(
                media_database=CARTOONS,
                media_type="Cartoon",
                library_name="Cartoon Library",
            )

        elif option == "3":
            media_type_menu(
                media_database=TV_SERIES,
                media_type="TV Series",
                library_name="TV Series Library",
            )

        elif option == "4":
            media_type_menu(
                media_database=MOVIES,
                media_type="Movie",
                library_name="Movie Library",
            )

        elif option == "5":
            print(
                "\nClosing Media Organizer..."
            )
            break

        else:
            print("\nInvalid option.")


if __name__ == "__main__":
    main()