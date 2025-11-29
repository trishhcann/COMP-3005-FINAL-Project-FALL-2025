# app/main.py

from app.member_service import member_menu
from app.trainer_service import trainer_menu
from app.admin_service import admin_menu


def main_menu():
    while True:
        print("\nHealth & Fitness Club Management System")
        print("1. Member")
        print("2. Trainer")
        print("3. Admin")
        print("0. Exit")

        choice = input("Please select if you are a member, trainer or admin staff: ").strip()

        if choice == "1":
            member_menu()
        elif choice == "2":
           trainer_menu()
        elif choice == "3":
            admin_menu()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main_menu()
