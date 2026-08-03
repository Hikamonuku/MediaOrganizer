from organizer import organize_series
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
        print("1. Organize anime")
        print("2. Organize TV series")
        print("3. Organize movies")
        print("4. Exit")

        option = input("\nSelect an option: ").strip()

        if option == "1":
            anime_menu()

        elif option == "2":
            print("\nTV series organizer is not implemented yet.")

        elif option == "3":
            print("\nMovie organizer is not implemented yet.")

        elif option == "4":
            print("\nClosing Media Organizer...")
            break

        else:
            print("\nInvalid option.")


if __name__ == "__main__":
    main()