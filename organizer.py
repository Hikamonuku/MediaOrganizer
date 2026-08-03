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
    filename_pattern: str,
) -> tuple[int, str | None] | None:
    # Trabalha com o nome sem a extensão.
    match = re.match(
        filename_pattern,
        file_path.stem,
        re.IGNORECASE,
    )
    if match is None:
        return None
    episode_number = int(match.group("episode"))
    groups = match.groupdict()
    title = groups.get("title")
    if title is not None:
        title = title.strip()
    return episode_number, title


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


def build_filename(
    series_name: str,
    season_number: int,
    season_episode: int,
    absolute_episode: int,
    extension: str,
    title: str | None,
    keep_title: bool,
) -> str:
    new_name = (
        f"{series_name} - "
        f"S{season_number:02d}E{season_episode:03d} - "
        f"{absolute_episode:03d}"
    )

    if keep_title and title:
        new_name += f" - {title}"

    return new_name + extension.lower()


def organize_series(path: str, series_data: dict) -> None:
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
            filename_pattern=series_data["filename_pattern"],
        )
        if episode_data is None:
            print(f"Ignored: {file_path.name}")
        ignored_files.append(file_path.name)
        continue
        absolute_episode, title = episode_dataa
        season_result = find_season(
            absolute_episode=absolute_episode,
            seasons=series_data["seasons"],
        )
        if season_result is None:
            print(f"Episode outside configured range: {file_path.name}")
            continue
        season_number, season_episode = season_result
        season_folder = folder / f"Season {season_number:02d}"
        new_filename = build_filename(
            series_name=series_data["name"],
            season_number=season_number,
            season_episode=season_episode,
            absolute_episode=absolute_episode,
            extension=file_path.suffix,
            title=title,
            keep_title=series_data["keep_title"],
        )
        planned_changes.append(
            {
                "source": file_path,
                "destination": season_folder / new_filename,
                "episode": absolute_episode,
            }
        )
    if not planned_changes:
        print("\nNo compatible episode files were found.")
        return
    planned_changes.sort(key=lambda item: item["episode"])
    print("\n==== Preview ====\n")
    for change in planned_changes:
        destination = change["destination"].relative_to(folder)
        print(change["source"].name)
        print(f"-> {destination}\n")
    found_episodes = {
        change["episode"]
        for change in planned_changes
    }
    expected_episodes = set(
        range(1, series_data["total_episodes"] + 1)
    )
    missing_episodes = sorted(
        expected_episodes - found_episodes
    )
    print(f"Compatible files: {len(planned_changes)}")
    print(f"Ignored files: {len(ignored_files)}")
    if missing_episodes:
        missing_text = ", ".join(
            f"{episode:03d}"
            for episode in missing_episodes
        )
        print(f"Missing episodes: {missing_text}")
    else:
        print("Missing episodes: none")
    confirmation = input("Apply these changes? (yes/no): ").strip().lower()
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