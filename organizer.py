import re
import shutil
from pathlib import Path

from database import VIDEO_EXTENSIONS


def prepare_folder(path: str) -> Path | None:
    folder = Path(path.strip().strip('"'))

    if not folder.exists():
        print("\nFolder not found.")
        return None

    if not folder.is_dir():
        print("\nThe provided path is not a folder.")
        return None

    return folder


def get_video_files(folder: Path) -> list[Path]:
    return sorted(
        [
            file_path
            for file_path in folder.rglob("*")
            if (
                file_path.is_file()
                and file_path.suffix.lower()
                in VIDEO_EXTENSIONS
            )
        ],
        key=lambda item: str(item).casefold(),
    )


def extract_episode_data(
    file_path: Path,
    filename_patterns: list[str],
) -> dict | None:
    for filename_pattern in filename_patterns:
        match = re.match(
            filename_pattern,
            file_path.stem.strip(),
            re.IGNORECASE,
        )

        if match is None:
            continue

        groups = match.groupdict()

        start_text = (
            groups.get("start")
            or groups.get("episode")
        )

        if start_text is None:
            continue

        start_episode = int(start_text)

        end_text = groups.get("end")
        end_episode = (
            int(end_text)
            if end_text
            else start_episode
        )

        if end_episode < start_episode:
            return None

        season_text = groups.get("season")
        season_number = (
            int(season_text)
            if season_text
            else None
        )

        title = groups.get("title")

        if title:
            title = title.strip()

        return {
            "season": season_number,
            "episodes": list(
                range(start_episode, end_episode + 1)
            ),
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
            return (
                season_data["season"],
                absolute_episode - start + 1,
            )

    return None


def build_episode_code(
    season: int,
    first_episode: int,
    last_episode: int,
    digits: int,
) -> str:
    code = (
        f"S{season:02d}"
        f"E{first_episode:0{digits}d}"
    )

    if first_episode != last_episode:
        code += (
            f"-E{last_episode:0{digits}d}"
        )

    return code


def build_filename(
    series_data: dict,
    season: int,
    season_episodes: list[int],
    absolute_episodes: list[int],
    extension: str,
    title: str | None,
) -> str:
    episode_code = build_episode_code(
        season=season,
        first_episode=season_episodes[0],
        last_episode=season_episodes[-1],
        digits=series_data["episode_digits"],
    )

    new_name = (
        f"{series_data['name']} - "
        f"{episode_code}"
    )

    if series_data["keep_absolute_number"]:
        first_absolute = absolute_episodes[0]
        last_absolute = absolute_episodes[-1]

        absolute_text = f"{first_absolute:03d}"

        if first_absolute != last_absolute:
            absolute_text += f"-{last_absolute:03d}"

        new_name += f" - {absolute_text}"

    if series_data["keep_title"] and title:
        new_name += f" - {title}"

    return new_name + extension.lower()


def create_change(
    root_folder: Path,
    file_path: Path,
    episode_data: dict,
    series_data: dict,
) -> dict | None:
    episodes = episode_data["episodes"]
    title = episode_data["title"]

    if series_data["numbering_mode"] == "season":
        season = episode_data["season"]

        if season is None:
            return None

        season_episodes = episodes

    else:
        first_result = find_season(
            episodes[0],
            series_data["seasons"],
        )

        last_result = find_season(
            episodes[-1],
            series_data["seasons"],
        )

        if first_result is None or last_result is None:
            return None

        first_season, first_season_episode = first_result
        last_season, last_season_episode = last_result

        if first_season != last_season:
            print(
                "Multi-episode file crosses seasons: "
                f"{file_path.name}"
            )
            return None

        season = first_season

        season_episodes = list(
            range(
                first_season_episode,
                last_season_episode + 1,
            )
        )

    destination_folder = (
        root_folder
        / f"Season {season:02d}"
    )

    destination = (
        destination_folder
        / build_filename(
            series_data=series_data,
            season=season,
            season_episodes=season_episodes,
            absolute_episodes=episodes,
            extension=file_path.suffix,
            title=title,
        )
    )

    return {
        "source": file_path,
        "destination": destination,
        "season": season,
        "season_episodes": season_episodes,
        "absolute_episodes": episodes,
    }


def find_duplicates(
    changes: list[dict],
    numbering_mode: str,
) -> dict:
    occurrences = {}

    for change in changes:
        if numbering_mode == "absolute":
            keys = change["absolute_episodes"]
        else:
            keys = [
                (change["season"], episode)
                for episode in change["season_episodes"]
            ]

        for key in keys:
            occurrences.setdefault(
                key,
                [],
            ).append(change["source"].name)

    return {
        key: filenames
        for key, filenames in occurrences.items()
        if len(filenames) > 1
    }


def find_missing(
    changes: list[dict],
    series_data: dict,
) -> list:
    if series_data["numbering_mode"] == "absolute":
        total = series_data.get("total_episodes")

        if total is None:
            return []

        found = {
            episode
            for change in changes
            for episode in change["absolute_episodes"]
        }

        return sorted(
            set(range(1, total + 1)) - found
        )

    expected = series_data.get(
        "expected_by_season"
    )

    if expected is None:
        return []

    found = {
        (change["season"], episode)
        for change in changes
        for episode in change["season_episodes"]
    }

    expected_keys = {
        (season, episode)
        for season, episodes in expected.items()
        for episode in episodes
    }

    return sorted(expected_keys - found)


def format_missing(
    missing: list,
    numbering_mode: str,
) -> str:
    if numbering_mode == "absolute":
        return ", ".join(
            f"{episode:03d}"
            for episode in missing
        )

    return ", ".join(
        f"S{season:02d}E{episode:02d}"
        for season, episode in missing
    )


def organize_series(
    path: str,
    series_data: dict,
    ask_confirmation: bool = True,
) -> dict:
    folder = prepare_folder(path)

    if folder is None:
        return {"status": "error"}

    if not series_data.get("enabled", True):
        print(
            f"\n{series_data['name']} is disabled."
        )
        print(series_data.get("note", ""))
        return {"status": "disabled"}

    changes = []
    ignored = []

    for file_path in get_video_files(folder):
        episode_data = extract_episode_data(
            file_path=file_path,
            filename_patterns=(
                series_data["filename_patterns"]
            ),
        )

        if episode_data is None:
            ignored.append(file_path)
            continue

        change = create_change(
            root_folder=folder,
            file_path=file_path,
            episode_data=episode_data,
            series_data=series_data,
        )

        if change is not None:
            # Já está exatamente no destino correto.
            if (
                file_path.resolve()
                == change["destination"].resolve()
            ):
                continue

            changes.append(change)

    if not changes:
        print(
            f"\n{series_data['name']}: "
            "nothing to organize."
        )

        return {
            "status": "nothing",
            "ignored": len(ignored),
        }

    duplicates = find_duplicates(
        changes=changes,
        numbering_mode=(
            series_data["numbering_mode"]
        ),
    )

    if duplicates:
        print("\n==== Duplicate Episodes ====\n")

        for episode, filenames in duplicates.items():
            print(f"{episode}:")

            for filename in filenames:
                print(f"  - {filename}")

        print(
            "\nNo files were moved because "
            "duplicates were found."
        )

        return {
            "status": "duplicates",
            "duplicates": duplicates,
        }

    changes.sort(
        key=lambda item: (
            item["season"],
            item["season_episodes"][0],
        )
    )

    print(
        f"\n==== Preview: "
        f"{series_data['name']} ====\n"
    )

    for change in changes:
        print(change["source"].relative_to(folder))
        print(
            "->",
            change["destination"].relative_to(folder),
            "\n",
        )

    missing = find_missing(
        changes=changes,
        series_data=series_data,
    )

    print(f"Files to organize: {len(changes)}")
    print(f"Ignored video files: {len(ignored)}")

    if missing:
        print(
            "Missing episodes: "
            + format_missing(
                missing,
                series_data["numbering_mode"],
            )
        )
    elif (
        series_data["numbering_mode"] == "absolute"
        or series_data.get("expected_by_season")
        is not None
    ):
        print("Missing episodes: none")
    else:
        print("Missing episodes: not configured")

    if ask_confirmation:
        confirmation = input(
            "\nApply these changes? (yes/no): "
        ).strip().lower()

        if confirmation not in {"yes", "y"}:
            print("\nOperation cancelled.")
            return {"status": "cancelled"}

    moved = 0
    skipped = 0

    for change in changes:
        source = change["source"]
        destination = change["destination"]

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if destination.exists():
            print(
                f"Skipped: {destination.name}"
            )
            skipped += 1
            continue

        try:
            shutil.move(
                str(source),
                str(destination),
            )
            moved += 1

        except OSError as error:
            print(
                f"Could not move "
                f"{source.name}: {error}"
            )
            skipped += 1

    print("\n==== Result ====")
    print(f"Moved: {moved}")
    print(f"Skipped: {skipped}")

    return {
        "status": "organized",
        "moved": moved,
        "skipped": skipped,
        "missing": missing,
    }