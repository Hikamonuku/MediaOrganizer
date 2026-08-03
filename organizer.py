import re
import shutil
from pathlib import Path


SEASONS = [
    {"season": 1, "start": 1, "end": 39},
    {"season": 2, "start": 40, "end": 74},
    {"season": 3, "start": 75, "end": 107},
    {"season": 4, "start": 108, "end": 139},
    {"season": 5, "start": 140, "end": 165},
    {"season": 6, "start": 166, "end": 194},
    {"season": 7, "start": 195, "end": 219},
    {"season": 8, "start": 220, "end": 253},
    {"season": 9, "start": 254, "end": 291},
]


def extract_episode_number(filename: str) -> int | None:
    match = re.search(
        r"DBZ_Episodio\s+(\d{3})",
        filename,
        re.IGNORECASE,
    )

    if match is None:
        return None

    return int(match.group(1))


def find_season(absolute_episode: int) -> tuple[int, int] | None:
    for season_data in SEASONS:
        if season_data["start"] <= absolute_episode <= season_data["end"]:
            season_number = season_data["season"]
            season_episode = absolute_episode - season_data["start"] + 1

            return season_number, season_episode

    return None


def build_new_filename(
    season_number: int,
    season_episode: int,
    absolute_episode: int,
    extension: str,
) -> str:
    return (
        f"Dragon Ball Z - "
        f"S{season_number:02d}E{season_episode:02d} - "
        f"{absolute_episode:03d}"
        f"{extension}"
    )


def organize_dbz(path: str) -> None:
    folder = Path(path.strip().strip('"'))

    if not folder.exists():
        print("\nFolder not found.")
        return

    if not folder.is_dir():
        print("\nThe provided path is not a folder.")
        return

    planned_changes = []
    ignored_files = []

    for file_path in folder.iterdir():
        if not file_path.is_file():
            continue

        episode_number = extract_episode_number(file_path.name)

        if episode_number is None:
            ignored_files.append(file_path.name)
            continue

        season_result = find_season(episode_number)

        if season_result is None:
            print(f"\nEpisode outside the configured range: {file_path.name}")
            continue

        season_number, season_episode = season_result

        season_folder = folder / f"Season {season_number:02d}"

        new_filename = build_new_filename(
            season_number=season_number,
            season_episode=season_episode,
            absolute_episode=episode_number,
            extension=file_path.suffix,
        )

        destination = season_folder / new_filename

        planned_changes.append(
            {
                "source": file_path,
                "destination": destination,
                "episode": episode_number,
            }
        )

    if not planned_changes:
        print("\nNo compatible Dragon Ball Z files were found.")
        return

    planned_changes.sort(key=lambda item: item["episode"])

    print("\n==== Preview ====\n")

    for change in planned_changes:
        source_name = change["source"].name
        destination_name = change["destination"].relative_to(folder)

        print(f"{source_name}")
        print(f"-> {destination_name}\n")

    print(f"Compatible files found: {len(planned_changes)}")
    print(f"Ignored files: {len(ignored_files)}")

    expected_episodes = set(range(1, 292))
    found_episodes = {
        change["episode"]
        for change in planned_changes
    }

    missing_episodes = sorted(expected_episodes - found_episodes)

    if missing_episodes:
        missing_text = ", ".join(
            f"{episode:03d}"
            for episode in missing_episodes
        )

        print(f"\nMissing episodes: {missing_text}")

    confirmation = input(
        "\nApply these changes? (yes/no): "
    ).strip().lower()

    if confirmation not in {"yes", "y"}:
        print("\nOperation cancelled.")
        return

    moved_files = 0
    skipped_files = 0

    for change in planned_changes:
        source = change["source"]
        destination = change["destination"]

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if destination.exists():
            print(f"Skipped: {destination.name} already exists.")
            skipped_files += 1
            continue

        try:
            shutil.move(
                str(source),
                str(destination),
            )
            moved_files += 1

        except OSError as error:
            print(f"Could not move {source.name}: {error}")
            skipped_files += 1

    print("\n==== Result ====")
    print(f"Moved files: {moved_files}")
    print(f"Skipped files: {skipped_files}")