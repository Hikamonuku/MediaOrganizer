import re
import shutil
from pathlib import Path


DBZ_SEASONS = [
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


def prepare_folder(path: str) -> Path | None:
    folder = Path(path.strip().strip('"'))

    if not folder.exists():
        print("\nFolder not found.")
        return None

    if not folder.is_dir():
        print("\nThe provided path is not a folder.")
        return None

    return folder


def apply_changes(
    folder: Path,
    planned_changes: list[dict],
    expected_episodes: set[int],
) -> None:
    if not planned_changes:
        print("\nNo compatible episode files were found.")
        return

    planned_changes.sort(key=lambda item: item["episode"])

    print("\n==== Preview ====\n")

    for change in planned_changes:
        source_name = change["source"].name
        destination = change["destination"].relative_to(folder)

        print(source_name)
        print(f"-> {destination}\n")

    found_episodes = {
        change["episode"]
        for change in planned_changes
    }

    missing_episodes = sorted(expected_episodes - found_episodes)

    print(f"Compatible files found: {len(planned_changes)}")

    if missing_episodes:
        missing_text = ", ".join(
            f"{episode:03d}"
            for episode in missing_episodes
        )
        print(f"Missing episodes: {missing_text}")
    else:
        print("Missing episodes: none")

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
            shutil.move(str(source), str(destination))
            moved_files += 1

        except OSError as error:
            print(f"Could not move {source.name}: {error}")
            skipped_files += 1

    print("\n==== Result ====")
    print(f"Moved files: {moved_files}")
    print(f"Skipped files: {skipped_files}")


# --------------------------------------------------
# Dragon Ball clássico
# --------------------------------------------------

def extract_dragon_ball_data(
    filename: str,
) -> tuple[int, str] | None:
    pattern = (
        r"^Dragon Ball\s+S\d+E(\d{3})\s*-\s*(.+)"
        r"(\.[^.]+)$"
    )

    match = re.match(pattern, filename, re.IGNORECASE)

    if match is None:
        return None

    episode_number = int(match.group(1))
    title = match.group(2).strip()

    return episode_number, title


def organize_dragon_ball(path: str) -> None:
    folder = prepare_folder(path)

    if folder is None:
        return

    planned_changes = []

    for file_path in folder.iterdir():
        if not file_path.is_file():
            continue

        episode_data = extract_dragon_ball_data(file_path.name)

        if episode_data is None:
            continue

        episode_number, title = episode_data

        if not 1 <= episode_number <= 153:
            print(f"Episode outside range: {file_path.name}")
            continue

        season_folder = folder / "Season 01"

        new_filename = (
            f"Dragon Ball - "
            f"S01E{episode_number:03d} - "
            f"{title}"
            f"{file_path.suffix}"
        )

        planned_changes.append(
            {
                "source": file_path,
                "destination": season_folder / new_filename,
                "episode": episode_number,
            }
        )

    apply_changes(
        folder=folder,
        planned_changes=planned_changes,
        expected_episodes=set(range(1, 154)),
    )


# --------------------------------------------------
# Dragon Ball Z
# --------------------------------------------------

def extract_dbz_episode_number(filename: str) -> int | None:
    match = re.search(
        r"DBZ_Episodio\s+(\d{3})",
        filename,
        re.IGNORECASE,
    )

    if match is None:
        return None

    return int(match.group(1))


def find_dbz_season(
    absolute_episode: int,
) -> tuple[int, int] | None:
    for season_data in DBZ_SEASONS:
        if season_data["start"] <= absolute_episode <= season_data["end"]:
            season_number = season_data["season"]

            season_episode = (
                absolute_episode
                - season_data["start"]
                + 1
            )

            return season_number, season_episode

    return None


def organize_dragon_ball_z(path: str) -> None:
    folder = prepare_folder(path)

    if folder is None:
        return

    planned_changes = []

    for file_path in folder.iterdir():
        if not file_path.is_file():
            continue

        absolute_episode = extract_dbz_episode_number(file_path.name)

        if absolute_episode is None:
            continue

        season_data = find_dbz_season(absolute_episode)

        if season_data is None:
            print(f"Episode outside range: {file_path.name}")
            continue

        season_number, season_episode = season_data
        season_folder = folder / f"Season {season_number:02d}"

        new_filename = (
            f"Dragon Ball Z - "
            f"S{season_number:02d}E{season_episode:02d} - "
            f"{absolute_episode:03d}"
            f"{file_path.suffix}"
        )

        planned_changes.append(
            {
                "source": file_path,
                "destination": season_folder / new_filename,
                "episode": absolute_episode,
            }
        )

    apply_changes(
        folder=folder,
        planned_changes=planned_changes,
        expected_episodes=set(range(1, 292)),
    )