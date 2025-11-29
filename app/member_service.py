# app/member_service.py

from datetime import datetime
from app.db import get_session
from models.member import Member
from models.health_metric import HealthMetric
from models.fitness_goal import FitnessGoal
from models.personal_training_session import PersonalTrainingSession
from models.class_registration import ClassRegistration


def member_menu():
    # Main menu for member related operations
    while True:
        print("\nMember Menu")
        print("1. Register new member")
        print("2. Update profile")
        print("3. Add health metric (health history)")
        print("4. View dashboard")
        print("5. View health history")
        print("0. Back to main menu")

        choice = input("Select an option: ").strip()

        if choice == "1":
            register_member()
        elif choice == "2":
            update_profile()
        elif choice == "3":
            add_health_metric()
        elif choice == "4":
            show_dashboard()
        elif choice == "5":
            view_health_history()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")


# Member operations

def register_member():
    # Create a new member 
    print("\nRegister New Member")
    first_name = input("First name: ").strip()
    last_name = input("Last name: ").strip()
    email = input("Email: ").strip()
    password = input("Password: ").strip()
    dob_str = input("Date of birth (YYYY-MM-DD, blank if none): ").strip()
    gender = input("Gender (optional): ").strip()
    phone = input("Phone (optional): ").strip()

    if not first_name or not last_name or not email or not password:
        print("First name, last name, email, and password are required.")
        return

    date_of_birth = None
    if dob_str:
        try:
            date_of_birth = datetime.strptime(dob_str, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Skipping date of birth.")

    session = get_session()
    try:
        # Check if email already exists
        existing = session.query(Member).filter_by(email=email).first()
        if existing:
            print("A member with that email already exists.")
            return

        member = Member(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password_hash=password,  
            date_of_birth=date_of_birth,
            gender=gender or None,
            phone=phone or None,
        )

        session.add(member)
        session.commit()
        print(f"Member registered with ID: {member.member_id}")
    except Exception as e:
        session.rollback()
        print("Error while registering member:", e)
    finally:
        session.close()


def find_member_by_email(session, email: str):
    # Helper to fetch a member by email
    return session.query(Member).filter_by(email=email).first()


def update_profile():
    # Update basic member profile info
    print("\nUpdate Profile")
    email = input("Enter your email: ").strip()
    if not email:
        print("Email is required.")
        return

    session = get_session()
    try:
        member = find_member_by_email(session, email)
        if not member:
            print("Member not found.")
            return

        print(f"\nUpdating profile for {member.first_name} {member.last_name} ({member.email})")
        print("Leave any field blank to keep the current value.\n")

        new_first = input(f"First name [{member.first_name}]: ").strip()
        new_last = input(f"Last name [{member.last_name}]: ").strip()
        new_phone = input(f"Phone [{member.phone or ''}]: ").strip()
        new_gender = input(f"Gender [{member.gender or ''}]: ").strip()
        new_dob = input(
            f"Date of birth (YYYY-MM-DD, blank to keep "
            f"{member.date_of_birth if member.date_of_birth else 'none'}): "
        ).strip()
        new_password = input("New password (blank to keep current): ").strip()

        if new_first:
            member.first_name = new_first
        if new_last:
            member.last_name = new_last
        if new_phone:
            member.phone = new_phone
        if new_gender:
            member.gender = new_gender
        if new_dob:
            try:
                member.date_of_birth = datetime.strptime(new_dob, "%Y-%m-%d").date()
            except ValueError:
                print("Invalid date format. Skipping DOB update.")
        if new_password:
            member.password_hash = new_password  

        session.commit()
        print("\nProfile updated successfully.")
    except Exception as e:
        session.rollback()
        print("Error while updating profile:", e)
    finally:
        session.close()



def add_health_metric():
    print("\nAdd Health Metric")
    email = input("Enter your email: ").strip()
    if not email:
        print("Email is required.")
        return

    session = get_session()
    try:
        member = find_member_by_email(session, email)
        if not member:
            print("Member not found.")
            return

        weight_str = input("Weight (kg, optional): ").strip()
        hr_str = input("Heart rate (bpm, optional): ").strip()
        bf_str = input("Body fat % (optional): ").strip()
        notes = input("Notes (optional): ").strip()

        weight = float(weight_str) if weight_str else None
        heart_rate = int(hr_str) if hr_str else None
        body_fat = float(bf_str) if bf_str else None

        metric = HealthMetric(
            member_id=member.member_id,
            weight=weight,
            heart_rate=heart_rate,
            body_fat_pct=body_fat,
            notes=notes or None,
        )

        session.add(metric)
        session.commit()
        print("Health metric added successfully.")
    except ValueError:
        session.rollback()
        print("Invalid numeric value for weight / heart rate / body fat.")
    except Exception as e:
        session.rollback()
        print("Error while adding health metric:", e)
    finally:
        session.close()


def show_dashboard():
    print("\n--- Member Dashboard ---")
    email = input("Enter your email: ").strip()
    if not email:
        print("Email is required.")
        return

    session = get_session()
    try:
        member = find_member_by_email(session, email)
        if not member:
            print("Member not found.")
            return

        print(f"\nDashboard for {member.first_name} {member.last_name} ({member.email})")

        # Latest health metric
        latest_metric = (
            session.query(HealthMetric)
            .filter_by(member_id=member.member_id)
            .order_by(HealthMetric.recorded_at.desc())
            .first()
        )

        if latest_metric:
            print("\nLatest Health Metric:")
            print(f"  Recorded at: {latest_metric.recorded_at}")
            print(f"  Weight:      {latest_metric.weight or 'N/A'} kg")
            print(f"  Heart rate:  {latest_metric.heart_rate or 'N/A'} bpm")
            print(f"  Body fat %:  {latest_metric.body_fat_pct or 'N/A'}")
        else:
            print("\nNo health metrics recorded yet.")

        # Active goals
        active_goals = (
            session.query(FitnessGoal)
            .filter_by(member_id=member.member_id, status="active")
            .all()
        )

        if active_goals:
            print("\nActive Fitness Goals:")
            for g in active_goals:
                print(f"  - {g.goal_type}: target {g.target_value} {g.unit} by {g.target_date or 'N/A'}")
        else:
            print("\nNo active fitness goals.")

        # Past classes count
        past_classes_count = (
            session.query(ClassRegistration)
            .filter(
                ClassRegistration.member_id == member.member_id,
                ClassRegistration.attendance_status == "attended",
            )
            .count()
        )
        print(f"\nTotal classes attended: {past_classes_count}")

        # Upcoming PT sessions
        now = datetime.utcnow()
        upcoming_sessions = (
            session.query(PersonalTrainingSession)
            .filter(
                PersonalTrainingSession.member_id == member.member_id,
                PersonalTrainingSession.start_time >= now,
            )
            .order_by(PersonalTrainingSession.start_time.asc())
            .all()
        )

        if upcoming_sessions:
            print("\nUpcoming Personal Training Sessions:")
            for s in upcoming_sessions:
                print(f"  - {s.start_time} to {s.end_time} (status: {s.status}) in room {s.room_id}")
        else:
            print("\nNo upcoming personal training sessions.")

    except Exception as e:
        print("Error while showing dashboard:", e)
    finally:
        session.close()

def view_health_history():
    print("\n--- View Health History ---")
    email = input("Enter your email: ").strip()
    if not email:
        print("Email is required.")
        return

    session = get_session()
    try:
        member = find_member_by_email(session, email)
        if not member:
            print("Member not found.")
            return

        metrics = (
            session.query(HealthMetric)
            .filter_by(member_id=member.member_id)
            .order_by(HealthMetric.recorded_at.desc())
            .all()
        )

        if not metrics:
            print("\nNo health metrics recorded yet.")
            return

        print(f"\nHealth History for {member.first_name} {member.last_name}:")
        print("---------------------------------------------------------")
        for m in metrics:
            print(f"{m.recorded_at} | Weight: {m.weight or 'N/A'} kg | "
                  f"HR: {m.heart_rate or 'N/A'} bpm | "
                  f"Body fat: {m.body_fat_pct or 'N/A'} | "
                  f"Notes: {m.notes or ''}")
        print("---------------------------------------------------------")

    except Exception as e:
        print("Error while viewing health history:", e)
    finally:
        session.close()

