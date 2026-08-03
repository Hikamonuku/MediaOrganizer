from organizer import organize_series
from scanner import scan_anime_library
from series import SERIES

def show_series_menu() -> None:
    print("\n==== Anime Organizer ====")

    for option, series_data in SERIES.items():
        print(f"{option}. {series_data['name']}")

    print("0. Back")


def anime_menu() -> None:
    while True:
        show_series_menu()

        option = input("\nSelect an anime: ").strip()

        if option == "0":
            return

        series_data = SERIES.get(option)

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


def main() -> None:
    while True:
        print("\n==== Media Organizer ====")
        print("1. Organize one anime")
        print("2. Scan anime library")
        print("3. Organize TV series")
        print("4. Organize movies")
        print("5. Exit")
        option = input(
            "\nSelect an option: "
        ).strip()
        if option == "1":
            anime_menu()
        elif option == "2":
            path = input(
                "\nAnime library folder: "
            )
            scan_anime_library(
                path=path,
                series_database=SERIES,
            )
        elif option == "3":
            print(
                "\nTV series organizer "
                "is not implemented yet."
            )
        elif option == "4":
            print(
                "\nMovie organizer "
                "is not implemented yet."
            )
        elif option == "5":
            print("\nClosing Media Organizer...")
            break
        else:
            print("\nInvalid option.")

if __name__ == "__main__":
    main()