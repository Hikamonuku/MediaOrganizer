import re
from collections import Counter
from pathlib import Path


AUDIOBOOK_EXTENSIONS = {
    ".mp3",
    ".wav",
    ".flac",
    ".m4a",
    ".aac",
    ".ogg",
    ".opus",
    ".wma",
}


def extract_chapter_number(file_path: Path) -> int | None:
    """
    Reconhece nomes como:

    01 - Introdução.mp3
    02 Produções e Salários.wav
    Capítulo 01.mp3
    Parte 03.mp3
    """

    patterns = [
        r"^(?P<number>\d{1,3})\b",
        r"^cap[ií]tulo\s+(?P<number>\d{1,3})\b",
        r"^parte\s+(?P<number>\d{1,3})\b",
    ]

    filename = file_path.stem.strip()

    for pattern in patterns:
        match = re.match(
            pattern,
            filename,
            re.IGNORECASE,
        )

        if match:
            return int(match.group("number"))

    return None


def find_missing_numbers(
    numbers: list[int],
) -> list[int]:
    if not numbers:
        return []

    unique_numbers = sorted(set(numbers))

    expected = set(
        range(
            unique_numbers[0],
            unique_numbers[-1] + 1,
        )
    )

    return sorted(
        expected - set(unique_numbers)
    )


def scan_book(book_folder: Path) -> dict:
    audio_files = sorted(
        [
            file_path
            for file_path in book_folder.rglob("*")
            if (
                file_path.is_file()
                and file_path.suffix.lower()
                in AUDIOBOOK_EXTENSIONS
            )
        ],
        key=lambda item: item.name.casefold(),
    )

    numbered_files = []
    unnumbered_files = []
    chapter_numbers = []

    for file_path in audio_files:
        chapter_number = extract_chapter_number(
            file_path
        )

        if chapter_number is None:
            unnumbered_files.append(file_path)
        else:
            numbered_files.append(file_path)
            chapter_numbers.append(chapter_number)

    number_occurrences = Counter(chapter_numbers)

    duplicate_numbers = {
        number: amount
        for number, amount
        in number_occurrences.items()
        if amount > 1
    }

    missing_numbers = find_missing_numbers(
        chapter_numbers
    )

    extensions = Counter(
        file_path.suffix.lower()
        for file_path in audio_files
    )

    return {
        "folder": book_folder,
        "audio_files": audio_files,
        "numbered_files": numbered_files,
        "unnumbered_files": unnumbered_files,
        "missing_numbers": missing_numbers,
        "duplicate_numbers": duplicate_numbers,
        "extensions": dict(
            sorted(extensions.items())
        ),
    }


def scan_audiobook_library(
    path: str,
) -> dict | None:
    library = Path(
        path.strip().strip('"')
    )

    if not library.exists():
        print("\nAudiobook library not found.")
        return None

    if not library.is_dir():
        print("\nThe provided path is not a folder.")
        return None

    authors = sorted(
        [
            item
            for item in library.iterdir()
            if item.is_dir()
        ],
        key=lambda item: item.name.casefold(),
    )

    books = []

    for author_folder in authors:
        book_folders = [
            item
            for item in author_folder.iterdir()
            if item.is_dir()
        ]

        # Caso o autor tenha os áudios diretamente na pasta.
        direct_audio_files = [
            item
            for item in author_folder.iterdir()
            if (
                item.is_file()
                and item.suffix.lower()
                in AUDIOBOOK_EXTENSIONS
            )
        ]

        if direct_audio_files:
            books.append(
                {
                    "author": author_folder.name,
                    "analysis": scan_book(
                        author_folder
                    ),
                }
            )

        for book_folder in sorted(
            book_folders,
            key=lambda item: item.name.casefold(),
        ):
            books.append(
                {
                    "author": author_folder.name,
                    "analysis": scan_book(
                        book_folder
                    ),
                }
            )

    print(
        "\n==== Audiobook Library Report ====\n"
    )

    total_audio_files = 0
    books_with_missing = 0
    books_with_duplicates = 0
    books_with_unnumbered = 0

    for item in books:
        author = item["author"]
        analysis = item["analysis"]

        total_audio_files += len(
            analysis["audio_files"]
        )

        if analysis["missing_numbers"]:
            books_with_missing += 1

        if analysis["duplicate_numbers"]:
            books_with_duplicates += 1

        if analysis["unnumbered_files"]:
            books_with_unnumbered += 1

        print(f"Author: {author}")
        print(
            f"Book: {analysis['folder'].name}"
        )
        print(
            "  Audio files: "
            f"{len(analysis['audio_files'])}"
        )
        print(
            "  Numbered chapters: "
            f"{len(analysis['numbered_files'])}"
        )
        print(
            "  Unnumbered files: "
            f"{len(analysis['unnumbered_files'])}"
        )

        if analysis["missing_numbers"]:
            missing_text = ", ".join(
                f"{number:02d}"
                for number
                in analysis["missing_numbers"]
            )

            print(
                f"  Missing numbers: "
                f"{missing_text}"
            )

        if analysis["duplicate_numbers"]:
            duplicate_text = ", ".join(
                (
                    f"{number:02d} "
                    f"({amount} files)"
                )
                for number, amount
                in analysis[
                    "duplicate_numbers"
                ].items()
            )

            print(
                f"  Duplicate numbers: "
                f"{duplicate_text}"
            )

        if analysis["extensions"]:
            formats = ", ".join(
                f"{extension}: {amount}"
                for extension, amount
                in analysis[
                    "extensions"
                ].items()
            )

            print(f"  Formats: {formats}")

        print()

    print("==== Summary ====")
    print(f"Authors: {len(authors)}")
    print(f"Books: {len(books)}")
    print(f"Audio files: {total_audio_files}")
    print(
        "Books with missing numbers: "
        f"{books_with_missing}"
    )
    print(
        "Books with duplicate numbers: "
        f"{books_with_duplicates}"
    )
    print(
        "Books with unnumbered files: "
        f"{books_with_unnumbered}"
    )

    return {
        "library": library,
        "authors": authors,
        "books": books,
        "total_audio_files": total_audio_files,
    }