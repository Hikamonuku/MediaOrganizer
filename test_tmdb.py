from Providers.tmdb import search_tv_series


def main() -> None:
    name = input("TV series name: ").strip()

    try:
        results = search_tv_series(name)

    except Exception as error:
        print(f"\nTMDb request failed: {error}")
        return

    if not results:
        print("\nNo results found.")
        return

    print("\n==== TMDb Results ====\n")

    for index, result in enumerate(results[:10], start=1):
        title = result.get("name", "Unknown title")
        original_title = result.get("original_name", "")
        first_air_date = result.get("first_air_date", "")
        year = first_air_date[:4] if first_air_date else "Unknown year"
        tmdb_id = result.get("id")

        print(f"{index}. {title} ({year})")

        if original_title and original_title != title:
            print(f"   Original title: {original_title}")

        print(f"   TMDb ID: {tmdb_id}\n")


if __name__ == "__main__":
    main()