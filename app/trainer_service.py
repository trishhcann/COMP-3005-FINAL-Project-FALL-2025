# app/trainer_service.py

from datetime import datetime
from app.db import get_session
from models.trainer import Trainer
from models.trainer_availability import TrainerAvailability
from models.personal_training_session import PersonalTrainingSession
from models.fitness_class import FitnessClass
from models.room import Room
from models.member import Member


def trainer_menu():
    # Main menu for trainer related operations
    while True:
        print("\nTrainer Menu")
        print("1. Set availability")
        print("2. View schedule (PT sessions + classes)")
        print("0. Back to main menu")

        choice = input("Select an option: ").strip()

        if choice == "1":
            set_availability()
        elif choice == "2":
            view_schedule()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")


# Helpers

def find_trainer_by_email(session, email: str):
    # Helper to fetch a trainer by email
    return session.query(Trainer).filter_by(email=email).first()


def parse_day_of_week():
    print("\nEnter day of week:")
    print("  1 = Monday, 2 = Tuesday, ..., 7 = Sunday")
    day_str = input("Day of week (1-7): ").strip()
    try:
        day = int(day_str)
        if day < 1 or day > 7:
            raise ValueError
        return day
    except ValueError:
        print("Invalid day. Please enter a number between 1 and 7.")
        return None


def parse_time(label: str):
    t_str = input(f"{label} time (HH:MM, 24-hour): ").strip()
    try:
        return datetime.strptime(t_str, "%H:%M").time()
    except ValueError:
        print("Invalid time format. Please use HH:MM (e.g. 09:30).")
        return None


# Trainer operations

def set_availability():
    print("\nSet Trainer Availability")
    email = input("Enter your trainer email: ").strip()
    if not email:
        print("Email is required.")
        return

    session = get_session()
    try:
        trainer = find_trainer_by_email(session, email)
        if not trainer:
            print("Trainer not found.")
            return

        day = parse_day_of_week()
        if day is None:
            return

        start_time = parse_time("Start")
        if start_time is None:
            return
        end_time = parse_time("End")
        if end_time is None:
            return

        if end_time <= start_time:
            print("End time must be after start time.")
            return

        # Check for overlapping availability on the same day
        existing_slots = (
            session.query(TrainerAvailability)
            .filter_by(trainer_id=trainer.trainer_id, day_of_week=day)
            .all()
        )

        for slot in existing_slots:
            # overlapping if new_start < existing_end AND new_end > existing_start
            if start_time < slot.end_time and end_time > slot.start_time:
                print(
                    "\nError: This availability overlaps with an existing slot:\n"
                    f"  Day {slot.day_of_week}, {slot.start_time}-{slot.end_time}"
                )
                return

        is_recurring_str = input("Is this recurring weekly? (y/n): ").strip().lower()
        is_recurring = is_recurring_str == "y"

        availability = TrainerAvailability(
            trainer_id=trainer.trainer_id,
            day_of_week=day,
            start_time=start_time,
            end_time=end_time,
            is_recurring=is_recurring,
        )

        session.add(availability)
        session.commit()
        print(
            f"\nAvailability added for {trainer.first_name} {trainer.last_name}: "
            f"day {day}, {start_time}-{end_time}, "
            f"{'recurring' if is_recurring else 'one-time'}."
        )
    except Exception as e:
        session.rollback()
        print("Error while setting availability:", e)
    finally:
        session.close()


def view_schedule():
    # Show upcoming PT sessions and classes for a trainer
    print("\nTrainer Schedule View")
    email = input("Enter your trainer email: ").strip()
    if not email:
        print("Email is required.")
        return

    session = get_session()
    try:
        trainer = find_trainer_by_email(session, email)
        if not trainer:
            print("Trainer not found.")
            return

        now = datetime.utcnow()

        # Upcoming PT sessions
        pt_sessions = (
            session.query(PersonalTrainingSession)
            .filter(
                PersonalTrainingSession.trainer_id == trainer.trainer_id,
                PersonalTrainingSession.start_time >= now,
            )
            .order_by(PersonalTrainingSession.start_time.asc())
            .all()
        )

        # Upcoming classes
        classes = (
            session.query(FitnessClass)
            .filter(
                FitnessClass.trainer_id == trainer.trainer_id,
                FitnessClass.start_time >= now,
            )
            .order_by(FitnessClass.start_time.asc())
            .all()
        )

        print(f"\nSchedule for {trainer.first_name} {trainer.last_name} ({trainer.email}):")

        # Print PT sessions
        if pt_sessions:
            print("\nUpcoming Personal Training Sessions:")
            print("------------------------------------------------")
            for s in pt_sessions:
                # Try to get related room and member info if available
                room_name = s.room.room_name if s.room else f"Room {s.room_id}"
                member_label = f"Member ID {s.member_id}"
                print(
                    f"{s.start_time} - {s.end_time} | {room_name} | "
                    f"{member_label} | status: {s.status}"
                )
            print("------------------------------------------------")
        else:
            print("\nNo upcoming personal training sessions.")

        # Print classes
        if classes:
            print("\nUpcoming Classes:")
            print("------------------------------------------------")
            for c in classes:
                room_name = c.room.room_name if c.room else f"Room {c.room_id}"
                print(
                    f"{c.start_time} - {c.end_time} | {c.class_name} | "
                    f"{room_name} | status: {c.status}"
                )
            print("------------------------------------------------")
        else:
            print("\nNo upcoming classes.")

    except Exception as e:
        print("Error while viewing schedule:", e)
    finally:
        session.close()
