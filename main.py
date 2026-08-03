from organizer import organize_dragon_ball
from organizer import organize_dragon_ball_z


def main():

    while True:

        print("\n==== Media Organizer ====")
        print("1 - Dragon Ball")
        print("2 - Dragon Ball Z")
        print("3 - Exit")

        option = input("\nSelect an option: ")

        if option == "1":

            path = input("\nDragon Ball folder: ")

            organize_dragon_ball(path)

        elif option == "2":

            path = input("\nDragon Ball Z folder: ")

            organize_dragon_ball_z(path)

        elif option == "3":

            print("\nClosing Media Organizer...")

            break

        else:

            print("\nInvalid option.")


if __name__ == "__main__":
    main()