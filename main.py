from organizer import organize_dbz


def main():

    print("==== Media Organizer ====\n")

    path = input("Dragon Ball Z folder: ")

    organize_dbz(path)


if __name__ == "__main__":
    main()