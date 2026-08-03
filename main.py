from organizer import organize_series
from scanner import scan_anime_library
from series import SERIES


def get_sorted_series() -> list[dict]:
    return sorted(
        SERIES.values(),
        key=lambda item: item["name"].casefold(),
    )


def show_series_menu() -> dict[str, dict]:
    print("\n==== Anime Organizer ====")

    menu_options = {}

    for index, series_data in enumerate(
        get_sorted_series(),
        start=1,
    ):
        option = str(index)
        menu_options[option] = series_data

        marker = (
            ""
            if series_data.get("enabled", True)
            else " [manual review]"
        )

        print(
            f"{option}. "
            f"{series_data['name']}"
            f"{marker}"
        )

    print("0. Back")

    return menu_options


def organize_one_anime() -> None:
    while True:
        menu_options = show_series_menu()

        option = input(
            "\nSelect an anime: "
        ).strip()

        if option == "0":
            return

        series_data = menu_options.get(option)

        if series_data is None:
            print("\nInvalid option.")
            continue

        path = input(
            f"\n{series_data['name']} folder: "
        )

        organize_series(
            path=path,
            series_data=series_data,
        )


def scan_library() -> None:
    path = input(
        "\nAnime library folder: "
    )

    scan_anime_library(
        path=path,
        series_database=SERIES,
    )


def organize_supported_library() -> None:
    path = input(
        "\nAnime library folder: "
    )

    report = scan_anime_library(
        path=path,
        series_database=SERIES,
    )

    if report is None:
        return

    supported = report["supported"]

    if not supported:
        print("\nNo supported anime found.")
        return

    print(
        "\nThe program will process only "
        "supported and enabled anime."
    )

    confirmation = input(
        "Continue? (yes/no): "
    ).strip().lower()

    if confirmation not in {"yes", "y"}:
        print("\nOperation cancelled.")
        return

    results = []

    for item in supported:
        anime_folder = item["folder"]
        series_data = item["series"]

        print(
            "\n\n================================"
        )
        print(series_data["name"])
        print(
            "================================"
        )

        result = organize_series(
            path=str(anime_folder),
            series_data=series_data,
            ask_confirmation=False,
        )

        results.append(
            {
                "name": series_data["name"],
                "result": result,
            }
        )

    print("\n==== Final Library Report ====\n")

    for item in results:
        status = item["result"].get(
            "status",
            "unknown",
        )

        print(
            f"{item['name']}: {status}"
        )


def main() -> None:
    while True:
        print("\n==== Media Organizer ====")
        print("1. Organize one anime")
        print("2. Scan anime library")
        print("3. Organize supported anime library")
        print("4. Organize TV series")
        print("5. Organize movies")
        print("6. Exit")

        option = input(
            "\nSelect an option: "
        ).strip()

        if option == "1":
            organize_one_anime()

        elif option == "2":
            scan_library()

        elif option == "3":
            organize_supported_library()

        elif option == "4":
            print(
                "\nTV series organizer "
                "is not implemented yet."
            )

        elif option == "5":
            print(
                "\nMovie organizer "
                "is not implemented yet."
            )

        elif option == "6":
            print(
                "\nClosing Media Organizer..."
            )
            break

        else:
            print("\nInvalid option.")


if __name__ == "__main__":
    main()