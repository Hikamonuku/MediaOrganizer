import re
import shutil
from pathlib import Path


def prepare_folder(path: str) -> Path | None:
    folder = Path(path.strip().strip('"'))

    if not folder.exists():
        print("\nFolder not found.")
        return None

    if not folder.is_dir():
        print("\nThe provided path is not a folder.")
        return None

    return folder


def extract_episode_data(
    file_path: Path,
    filename_patterns: list[str],
) -> dict | None:
    """
    Retorna algo como:

    {
        "season": None,
        "episodes": [52, 53],
        "title": None,
    }
    """

    for filename_pattern in filename_patterns:
        match = re.match(
            filename_pattern,
            file_path.stem,
            re.IGNORECASE,
        )

        if match is None:
            continue

        groups = match.groupdict()

        start_episode = int(groups["start"])

        end_text = groups.get("end")
        end_episode = (
            int(end_text)
            if end_text is not None
            else start_episode
        )

        if end_episode < start_episode:
            return None

        episodes = list(
            range(start_episode, end_episode + 1)
        )

        season_text = groups.get("season")
        season_number = (
            int(season_text)
            if season_text is not None
            else None
        )

        title = groups.get("title")

        if title is not None:
            title = title.strip()

        return {
            "season": season_number,
            "episodes": episodes,
            "title": title,
        }

    return None


def find_season(
    absolute_episode: int,
    seasons: list[dict],
) -> tuple[int, int] | None:
    for season_data in seasons:
        start = season_data["start"]
        end = season_data["end"]

        if start <= absolute_episode <= end:
            season_number = season_data["season"]
            season_episode = absolute_episode - start + 1

            return season_number, season_episode

    return None


def format_episode_code(
    season_number: int,
    first_episode: int,
    last_episode: int,
    episode_digits: int,
) -> str:
    first_code = (
        f"S{season_number:02d}"
        f"E{first_episode:0{episode_digits}d}"
    )

    if first_episode == last_episode:
        return first_code

    return (
        f"{first_code}"
        f"-E{last_episode:0{episode_digits}d}"
    )


def format_absolute_number(
    episodes: list[int],
) -> str:
    first_episode = episodes[0]
    last_episode = episodes[-1]

    if first_episode == last_episode:
        return f"{first_episode:03d}"

    return (
        f"{first_episode:03d}"
        f"-{last_episode:03d}"
    )


def build_filename(
    series_name: str,
    season_number: int,
    first_season_episode: int,
    last_season_episode: int,
    absolute_episodes: list[int],
    extension: str,
    title: str | None,
    keep_title: bool,
    keep_absolute_number: bool,
    episode_digits: int,
) -> str:
    episode_code = format_episode_code(
        season_number=season_number,
        first_episode=first_season_episode,
        last_episode=last_season_episode,
        episode_digits=episode_digits,
    )

    new_name = f"{series_name} - {episode_code}"

    if keep_absolute_number:
        absolute_text = format_absolute_number(
            absolute_episodes
        )

        new_name += f" - {absolute_text}"

    if keep_title and title:
        new_name += f" - {title}"

    return new_name + extension.lower()


def create_change(
    folder: Path,
    file_path: Path,
    episode_data: dict,
    series_data: dict,
) -> dict | None:
    numbering_mode = series_data["numbering_mode"]
    episodes = episode_data["episodes"]
    title = episode_data["title"]

    if numbering_mode == "absolute":
        first_result = find_season(
            absolute_episode=episodes[0],
            seasons=series_data["seasons"],
        )

        last_result = find_season(
            absolute_episode=episodes[-1],
            seasons=series_data["seasons"],
        )

        if first_result is None or last_result is None:
            print(
                f"Episode outside configured range: "
                f"{file_path.name}"
            )
            return None

        first_season, first_season_episode = first_result
        last_season, last_season_episode = last_result

        # Um episódio duplo não pode atravessar duas temporadas.
        if first_season != last_season:
            print(
                f"Multi-episode file crosses seasons: "
                f"{file_path.name}"
            )
            return None

        season_number = first_season

    elif numbering_mode == "season":
        season_number = episode_data["season"]

        if season_number is None:
            print(
                f"Season number not found: "
                f"{file_path.name}"
            )
            return None

        first_season_episode = episodes[0]
        last_season_episode = episodes[-1]

    else:
        print(
            f"Unknown numbering mode: "
            f"{numbering_mode}"
        )
        return None

    season_folder = (
        folder
        / f"Season {season_number:02d}"
    )

    new_filename = build_filename(
        series_name=series_data["name"],
        season_number=season_number,
        first_season_episode=first_season_episode,
        last_season_episode=last_season_episode,
        absolute_episodes=episodes,
        extension=file_path.suffix,
        title=title,
        keep_title=series_data["keep_title"],
        keep_absolute_number=(
            series_data["keep_absolute_number"]
        ),
        episode_digits=series_data["episode_digits"],
    )

    return {
        "source": file_path,
        "destination": season_folder / new_filename,
        "episodes": episodes,
        "season": season_number,
        "season_episodes": list(
            range(
                first_season_episode,
                last_season_episode + 1,
            )
        ),
    }


def find_duplicates(
    planned_changes: list[dict],
    numbering_mode: str,
) -> dict:
    episode_files: dict = {}

    for change in planned_changes:
        if numbering_mode == "absolute":
            episode_keys = change["episodes"]
        else:
            episode_keys = [
                (change["season"], episode)
                for episode in change["season_episodes"]
            ]

        for episode_key in episode_keys:
            episode_files.setdefault(
                episode_key,
                [],
            ).append(change["source"].name)

    return {
        episode: filenames
        for episode, filenames in episode_files.items()
        if len(filenames) > 1
    }


def show_duplicates(
    duplicates: dict,
    numbering_mode: str,
) -> None:
    print("\n==== Duplicate Episodes ====\n")

    for episode, filenames in duplicates.items():
        if numbering_mode == "absolute":
            episode_label = f"{episode:03d}"
        else:
            season, season_episode = episode
            episode_label = (
                f"S{season:02d}E{season_episode:02d}"
            )

        print(f"Episode {episode_label}:")

        for filename in filenames:
            print(f"  - {filename}")

        print()


def find_missing_episodes(
    planned_changes: list[dict],
    series_data: dict,
) -> list:
    numbering_mode = series_data["numbering_mode"]

    if numbering_mode == "absolute":
        found_episodes = {
            episode
            for change in planned_changes
            for episode in change["episodes"]
        }

        expected_episodes = set(
            range(
                1,
                series_data["total_episodes"] + 1,
            )
        )

        return sorted(
            expected_episodes - found_episodes
        )

    found_episodes = {
        (change["season"], episode)
        for change in planned_changes
        for episode in change["season_episodes"]
    }

    expected_episodes = {
        (season, episode)
        for season, episodes
        in series_data["expected_by_season"].items()
        for episode in episodes
    }

    return sorted(
        expected_episodes - found_episodes
    )


def format_missing_episodes(
    missing_episodes: list,
    numbering_mode: str,
) -> str:
    if numbering_mode == "absolute":
        return ", ".join(
            f"{episode:03d}"
            for episode in missing_episodes
        )

    return ", ".join(
        f"S{season:02d}E{episode:02d}"
        for season, episode in missing_episodes
    )


def organize_series(
    path: str,
    series_data: dict,
) -> None:
    folder = prepare_folder(path)

    if folder is None:
        return

    planned_changes = []
    ignored_files = []

    for file_path in folder.iterdir():
        if not file_path.is_file():
            continue

        episode_data = extract_episode_data(
            file_path=file_path,
            filename_patterns=(
                series_data["filename_patterns"]
            ),
        )

        if episode_data is None:
            ignored_files.append(file_path.name)
            continue

        change = create_change(
            folder=folder,
            file_path=file_path,
            episode_data=episode_data,
            series_data=series_data,
        )

        if change is not None:
            planned_changes.append(change)

    if not planned_changes:
        print("\nNo compatible episode files were found.")
        return

    planned_changes.sort(
        key=lambda item: (
            item["season"],
            item["season_episodes"][0],
        )
    )

    duplicates = find_duplicates(
        planned_changes=planned_changes,
        numbering_mode=series_data["numbering_mode"],
    )

    if duplicates:
        show_duplicates(
            duplicates=duplicates,
            numbering_mode=(
                series_data["numbering_mode"]
            ),
        )

        print(
            "Remove or separate the duplicate files "
            "before organizing this series."
        )
        print(
            "No files were renamed or moved."
        )
        return

    print("\n==== Preview ====\n")

    for change in planned_changes:
        destination = (
            change["destination"]
            .relative_to(folder)
        )

        print(change["source"].name)
        print(f"-> {destination}\n")

    missing_episodes = find_missing_episodes(
        planned_changes=planned_changes,
        series_data=series_data,
    )

    print(
        f"Compatible files: "
        f"{len(planned_changes)}"
    )
    print(
        f"Ignored files: "
        f"{len(ignored_files)}"
    )

    if missing_episodes:
        missing_text = format_missing_episodes(
            missing_episodes=missing_episodes,
            numbering_mode=(
                series_data["numbering_mode"]
            ),
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
            print(
                f"Skipped: {destination.name} "
                f"already exists."
            )
            skipped_files += 1
            continue

        try:
            shutil.move(
                str(source),
                str(destination),
            )
            moved_files += 1

        except OSError as error:
            print(
                f"Could not move "
                f"{source.name}: {error}"
            )
            skipped_files += 1

    print("\n==== Result ====")
    print(f"Moved files: {moved_files}")
    print(f"Skipped files: {skipped_files}")