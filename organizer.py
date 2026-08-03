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
    """
    Procura arquivos de vídeo na pasta principal
    e em todas as subpastas.
    """
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
    """
    Tenta reconhecer temporada, episódio, título
    e arquivos com múltiplos episódios.

    Retorno de exemplo:

    {
        "season": 1,
        "episodes": [4],
        "title": "Episode title",
    }

    Arquivo duplo:

    {
        "season": 1,
        "episodes": [4, 5],
        "title": None,
    }
    """
    filename = file_path.stem.strip()

    for filename_pattern in filename_patterns:
        match = re.match(
            filename_pattern,
            filename,
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

        if end_text:
            end_episode = int(end_text)
        else:
            end_episode = start_episode

        if end_episode < start_episode:
            return None

        season_text = groups.get("season")

        if season_text:
            season_number = int(season_text)
        else:
            season_number = None

        title = groups.get("title")

        if title:
            title = title.strip()

        return {
            "season": season_number,
            "episodes": list(
                range(
                    start_episode,
                    end_episode + 1,
                )
            ),
            "title": title,
        }

    return None


def find_season(
    absolute_episode: int,
    seasons: list[dict],
) -> tuple[int, int] | None:
    """
    Converte um episódio absoluto em:

    (temporada, episódio dentro da temporada)
    """
    for season_data in seasons:
        start = season_data["start"]
        end = season_data["end"]

        if start <= absolute_episode <= end:
            season_number = season_data["season"]
            season_episode = (
                absolute_episode
                - start
                + 1
            )

            return (
                season_number,
                season_episode,
            )

    return None


def build_episode_code(
    season_number: int,
    first_episode: int,
    last_episode: int,
    episode_digits: int,
) -> str:
    """
    Cria:

    S01E01

    ou:

    S01E01-E02
    """
    code = (
        f"S{season_number:02d}"
        f"E{first_episode:0{episode_digits}d}"
    )

    if first_episode != last_episode:
        code += (
            f"-E{last_episode:0{episode_digits}d}"
        )

    return code


def build_absolute_text(
    absolute_episodes: list[int],
) -> str:
    first_episode = absolute_episodes[0]
    last_episode = absolute_episodes[-1]

    if first_episode == last_episode:
        return f"{first_episode:03d}"

    return (
        f"{first_episode:03d}"
        f"-{last_episode:03d}"
    )


def build_filename(
    series_data: dict,
    season_number: int,
    season_episodes: list[int],
    absolute_episodes: list[int],
    extension: str,
    title: str | None,
) -> str:
    episode_code = build_episode_code(
        season_number=season_number,
        first_episode=season_episodes[0],
        last_episode=season_episodes[-1],
        episode_digits=series_data["episode_digits"],
    )

    new_name = (
        f"{series_data['name']} - "
        f"{episode_code}"
    )

    if series_data.get(
        "keep_absolute_number",
        False,
    ):
        absolute_text = build_absolute_text(
            absolute_episodes
        )

        new_name += f" - {absolute_text}"

    if (
        series_data.get("keep_title", False)
        and title
    ):
        new_name += f" - {title}"

    return (
        new_name
        + extension.lower()
    )


def create_file_record(
    root_folder: Path,
    file_path: Path,
    episode_data: dict,
    series_data: dict,
) -> dict | None:
    """
    Cria o registro completo de um arquivo reconhecido.

    Esse registro é usado tanto para análise quanto
    para movimentação.
    """
    source_episodes = episode_data["episodes"]
    title = episode_data["title"]

    numbering_mode = series_data["numbering_mode"]

    if numbering_mode == "season":
        season_number = episode_data["season"]

        if season_number is None:
            print(
                "Season number not found: "
                f"{file_path.name}"
            )
            return None

        season_episodes = source_episodes
        absolute_episodes = source_episodes

    elif numbering_mode == "absolute":
        first_result = find_season(
            absolute_episode=source_episodes[0],
            seasons=series_data["seasons"],
        )

        last_result = find_season(
            absolute_episode=source_episodes[-1],
            seasons=series_data["seasons"],
        )

        if (
            first_result is None
            or last_result is None
        ):
            print(
                "Episode outside configured range: "
                f"{file_path.name}"
            )
            return None

        (
            first_season,
            first_season_episode,
        ) = first_result

        (
            last_season,
            last_season_episode,
        ) = last_result

        if first_season != last_season:
            print(
                "Multi-episode file crosses seasons: "
                f"{file_path.name}"
            )
            return None

        season_number = first_season

        season_episodes = list(
            range(
                first_season_episode,
                last_season_episode + 1,
            )
        )

        absolute_episodes = source_episodes

    else:
        print(
            "Unknown numbering mode: "
            f"{numbering_mode}"
        )
        return None

    season_folder = (
        root_folder
        / f"Season {season_number:02d}"
    )

    new_filename = build_filename(
        series_data=series_data,
        season_number=season_number,
        season_episodes=season_episodes,
        absolute_episodes=absolute_episodes,
        extension=file_path.suffix,
        title=title,
    )

    destination = (
        season_folder
        / new_filename
    )

    already_organized = (
        file_path.resolve()
        == destination.resolve()
    )

    return {
        "source": file_path,
        "destination": destination,
        "season": season_number,
        "season_episodes": season_episodes,
        "absolute_episodes": absolute_episodes,
        "title": title,
        "already_organized": already_organized,
    }


def get_episode_keys(
    record: dict,
    numbering_mode: str,
) -> list:
    """
    Retorna as chaves usadas para detectar
    episódios repetidos.
    """
    if numbering_mode == "absolute":
        return record["absolute_episodes"]

    return [
        (
            record["season"],
            episode,
        )
        for episode in record["season_episodes"]
    ]


def find_duplicates(
    recognized_files: list[dict],
    numbering_mode: str,
) -> dict:
    occurrences = {}

    for record in recognized_files:
        episode_keys = get_episode_keys(
            record=record,
            numbering_mode=numbering_mode,
        )

        for episode_key in episode_keys:
            occurrences.setdefault(
                episode_key,
                [],
            ).append(
                record["source"]
            )

    return {
        episode_key: file_paths
        for episode_key, file_paths
        in occurrences.items()
        if len(file_paths) > 1
    }


def find_destination_conflicts(
    pending_changes: list[dict],
) -> list[dict]:
    """
    Detecta casos em que o arquivo de destino já existe,
    mas não é o próprio arquivo analisado.
    """
    conflicts = []

    for record in pending_changes:
        destination = record["destination"]

        if destination.exists():
            conflicts.append(record)

    return conflicts


def find_missing_episodes(
    recognized_files: list[dict],
    series_data: dict,
) -> list:
    """
    Usa todos os arquivos reconhecidos.

    Isso inclui:
    - arquivos já organizados;
    - arquivos que ainda serão movidos.
    """
    numbering_mode = series_data["numbering_mode"]

    if numbering_mode == "absolute":
        total_episodes = series_data.get(
            "total_episodes"
        )

        if total_episodes is None:
            return []

        found_episodes = {
            episode
            for record in recognized_files
            for episode
            in record["absolute_episodes"]
        }

        expected_episodes = set(
            range(
                1,
                total_episodes + 1,
            )
        )

        return sorted(
            expected_episodes
            - found_episodes
        )

    expected_by_season = series_data.get(
        "expected_by_season"
    )

    if expected_by_season is None:
        return []

    found_episodes = {
        (
            record["season"],
            episode,
        )
        for record in recognized_files
        for episode in record["season_episodes"]
    }

    expected_episodes = {
        (
            season_number,
            episode,
        )
        for season_number, episodes
        in expected_by_season.items()
        for episode in episodes
    }

    return sorted(
        expected_episodes
        - found_episodes
    )


def format_episode_key(
    episode_key,
    numbering_mode: str,
) -> str:
    if numbering_mode == "absolute":
        return f"{episode_key:03d}"

    season_number, episode_number = episode_key

    return (
        f"S{season_number:02d}"
        f"E{episode_number:02d}"
    )


def format_missing_episodes(
    missing_episodes: list,
    numbering_mode: str,
) -> str:
    return ", ".join(
        format_episode_key(
            episode_key=episode,
            numbering_mode=numbering_mode,
        )
        for episode in missing_episodes
    )


def determine_status(
    analysis: dict,
) -> str:
    if analysis["duplicates"]:
        return "duplicates"

    if analysis["destination_conflicts"]:
        return "conflicts"

    if not analysis["recognized_files"]:
        return "no-compatible-files"

    if analysis["pending_changes"]:
        if analysis["missing_episodes"]:
            return "ready-incomplete"

        return "ready"

    if analysis["missing_episodes"]:
        return "organized-incomplete"

    return "already-organized"


def analyze_series(
    path: str,
    series_data: dict,
) -> dict:
    """
    Analisa a série sem mover nenhum arquivo.
    """
    folder = prepare_folder(path)

    if folder is None:
        return {
            "status": "error",
            "folder": None,
            "series_data": series_data,
            "recognized_files": [],
            "pending_changes": [],
            "already_organized": [],
            "ignored_files": [],
            "duplicates": {},
            "destination_conflicts": [],
            "missing_episodes": [],
        }

    if not series_data.get("enabled", True):
        return {
            "status": "disabled",
            "folder": folder,
            "series_data": series_data,
            "recognized_files": [],
            "pending_changes": [],
            "already_organized": [],
            "ignored_files": [],
            "duplicates": {},
            "destination_conflicts": [],
            "missing_episodes": [],
        }

    recognized_files = []
    pending_changes = []
    already_organized = []
    ignored_files = []

    for file_path in get_video_files(folder):
        episode_data = extract_episode_data(
            file_path=file_path,
            filename_patterns=(
                series_data["filename_patterns"]
            ),
        )

        if episode_data is None:
            ignored_files.append(file_path)
            continue

        record = create_file_record(
            root_folder=folder,
            file_path=file_path,
            episode_data=episode_data,
            series_data=series_data,
        )

        if record is None:
            ignored_files.append(file_path)
            continue

        recognized_files.append(record)

        if record["already_organized"]:
            already_organized.append(record)
        else:
            pending_changes.append(record)

    duplicates = find_duplicates(
        recognized_files=recognized_files,
        numbering_mode=(
            series_data["numbering_mode"]
        ),
    )

    destination_conflicts = (
        find_destination_conflicts(
            pending_changes=pending_changes,
        )
    )

    missing_episodes = find_missing_episodes(
        recognized_files=recognized_files,
        series_data=series_data,
    )

    analysis = {
        "status": "",
        "folder": folder,
        "series_data": series_data,
        "recognized_files": recognized_files,
        "pending_changes": pending_changes,
        "already_organized": already_organized,
        "ignored_files": ignored_files,
        "duplicates": duplicates,
        "destination_conflicts": (
            destination_conflicts
        ),
        "missing_episodes": missing_episodes,
    }

    analysis["status"] = determine_status(
        analysis
    )

    return analysis


def show_duplicates(
    analysis: dict,
) -> None:
    duplicates = analysis["duplicates"]
    numbering_mode = analysis[
        "series_data"
    ]["numbering_mode"]

    print("\n==== Duplicate Episodes ====\n")

    for episode_key, file_paths in duplicates.items():
        episode_text = format_episode_key(
            episode_key=episode_key,
            numbering_mode=numbering_mode,
        )

        print(f"{episode_text}:")

        for file_path in file_paths:
            relative_path = file_path.relative_to(
                analysis["folder"]
            )

            print(f"  - {relative_path}")

        print()


def show_destination_conflicts(
    analysis: dict,
) -> None:
    print("\n==== Destination Conflicts ====\n")

    for record in analysis[
        "destination_conflicts"
    ]:
        source = record["source"].relative_to(
            analysis["folder"]
        )

        destination = record[
            "destination"
        ].relative_to(
            analysis["folder"]
        )

        print(source)
        print(f"  -> {destination}")
        print("  Destination already exists.\n")


def show_analysis(
    analysis: dict,
    show_preview: bool = True,
) -> None:
    series_data = analysis["series_data"]
    folder = analysis["folder"]

    print(
        f"\n==== Analysis: "
        f"{series_data['name']} ====\n"
    )

    if analysis["status"] == "error":
        return

    if analysis["status"] == "disabled":
        print("Status: manual review / disabled")

        note = series_data.get("note", "")

        if note:
            print(f"Note: {note}")

        return

    if show_preview and analysis["pending_changes"]:
        print("==== Pending Changes ====\n")

        sorted_changes = sorted(
            analysis["pending_changes"],
            key=lambda item: (
                item["season"],
                item["season_episodes"][0],
            ),
        )

        for record in sorted_changes:
            source = record["source"].relative_to(
                folder
            )

            destination = record[
                "destination"
            ].relative_to(
                folder
            )

            print(source)
            print(f"-> {destination}\n")

    print("==== Summary ====")
    print(
        "Recognized video files: "
        f"{len(analysis['recognized_files'])}"
    )
    print(
        "Already organized: "
        f"{len(analysis['already_organized'])}"
    )
    print(
        "Pending changes: "
        f"{len(analysis['pending_changes'])}"
    )
    print(
        "Ignored video files: "
        f"{len(analysis['ignored_files'])}"
    )
    print(
        "Duplicate episodes: "
        f"{len(analysis['duplicates'])}"
    )
    print(
        "Destination conflicts: "
        f"{len(analysis['destination_conflicts'])}"
    )

    missing_episodes = analysis[
        "missing_episodes"
    ]

    if missing_episodes:
        missing_text = format_missing_episodes(
            missing_episodes=missing_episodes,
            numbering_mode=(
                series_data["numbering_mode"]
            ),
        )

        print(
            f"Missing episodes: {missing_text}"
        )

    elif (
        series_data["numbering_mode"]
        == "absolute"
        or series_data.get(
            "expected_by_season"
        )
        is not None
    ):
        print("Missing episodes: none")

    else:
        print(
            "Missing episodes: "
            "not configured"
        )

    print(
        f"Status: {analysis['status']}"
    )

    if analysis["duplicates"]:
        show_duplicates(analysis)

    if analysis["destination_conflicts"]:
        show_destination_conflicts(
            analysis
        )


def apply_changes(
    analysis: dict,
) -> dict:
    """
    Aplica somente os arquivos pendentes.
    """
    if analysis["status"] in {
        "error",
        "disabled",
        "duplicates",
        "conflicts",
        "no-compatible-files",
    }:
        return {
            "status": analysis["status"],
            "moved": 0,
            "skipped": 0,
            "missing": analysis.get(
                "missing_episodes",
                [],
            ),
        }

    pending_changes = sorted(
        analysis["pending_changes"],
        key=lambda item: (
            item["season"],
            item["season_episodes"][0],
        ),
    )

    if not pending_changes:
        return {
            "status": analysis["status"],
            "moved": 0,
            "skipped": 0,
            "missing": analysis[
                "missing_episodes"
            ],
        }

    moved_files = 0
    skipped_files = 0

    for record in pending_changes:
        source = record["source"]
        destination = record["destination"]

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if destination.exists():
            print(
                "Skipped: destination already exists: "
                f"{destination.name}"
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
                f"{source.name}: "
                f"{error}"
            )

            skipped_files += 1

    status = "organized"

    if skipped_files:
        status = "organized-with-skips"

    return {
        "status": status,
        "moved": moved_files,
        "skipped": skipped_files,
        "missing": analysis[
            "missing_episodes"
        ],
    }


def organize_series(
    path: str,
    series_data: dict,
    ask_confirmation: bool = True,
) -> dict:
    """
    Função principal usada pelo main.py.

    1. Analisa.
    2. Mostra o relatório.
    3. Bloqueia conflitos e duplicados.
    4. Pede confirmação.
    5. Aplica as mudanças.
    """
    analysis = analyze_series(
        path=path,
        series_data=series_data,
    )

    show_analysis(
        analysis=analysis,
        show_preview=True,
    )

    blocked_statuses = {
        "error",
        "disabled",
        "duplicates",
        "conflicts",
        "no-compatible-files",
    }

    if analysis["status"] in blocked_statuses:
        if analysis["status"] == "duplicates":
            print(
                "\nNo files were moved because "
                "duplicate episodes were found."
            )

        elif analysis["status"] == "conflicts":
            print(
                "\nNo files were moved because "
                "destination conflicts were found."
            )

        elif (
            analysis["status"]
            == "no-compatible-files"
        ):
            print(
                "\nNo compatible episode files "
                "were found."
            )

        return {
            "status": analysis["status"],
            "moved": 0,
            "skipped": 0,
            "missing": analysis[
                "missing_episodes"
            ],
        }

    if not analysis["pending_changes"]:
        print(
            "\nThere are no pending changes."
        )

        return {
            "status": analysis["status"],
            "moved": 0,
            "skipped": 0,
            "missing": analysis[
                "missing_episodes"
            ],
        }

    if ask_confirmation:
        confirmation = input(
            "\nApply these changes? "
            "(yes/no): "
        ).strip().lower()

        if confirmation not in {"yes", "y"}:
            print("\nOperation cancelled.")

            return {
                "status": "cancelled",
                "moved": 0,
                "skipped": 0,
                "missing": analysis[
                    "missing_episodes"
                ],
            }

    result = apply_changes(
        analysis=analysis
    )

    print("\n==== Result ====")
    print(f"Moved files: {result['moved']}")
    print(f"Skipped files: {result['skipped']}")

    if result["missing"]:
        print(
            "The collection remains incomplete."
        )
    else:
        print(
            "No configured episodes are missing."
        )

    return result