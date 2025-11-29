# app/admin_service.py

from datetime import datetime
from app.db import get_session
from models.admin_staff import AdminStaff
from models.trainer import Trainer
from models.room import Room
from models.fitness_class import FitnessClass
from models.equipment import Equipment
from models.equipment_maintenance import EquipmentMaintenance


def admin_menu():
    # Main menu for admin-related operations
    while True:
        print("\nAdmin Menu")
        print("1. Create class / book room")
        print("2. Log equipment issue")
        print("3. Update equipment maintenance status")
        print("0. Back to main menu")

        choice = input("Select an option: ").strip()

        if choice == "1":
            create_class_booking()
        elif choice == "2":
            log_equipment_issue()
        elif choice == "3":
            update_maintenance_issue()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")


# Helpers

def find_admin_by_email(session, email: str):
    return session.query(AdminStaff).filter_by(email=email).first()


def find_trainer_by_email(session, email: str):
    return session.query(Trainer).filter_by(email=email).first()


def parse_datetime(label: str):
    dt_str = input(f"{label} (YYYY-MM-DD HH:MM): ").strip()
    try:
        return datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
    except ValueError:
        print("Invalid datetime format. Please use YYYY-MM-DD HH:MM.")
        return None


# Room booking / class

def create_class_booking():
    # Admins create a class which books a room and trainer
    print("\nCreate Class / Book Room")
    admin_email = input("Enter your admin email: ").strip()
    if not admin_email:
        print("Admin email is required.")
        return

    session = get_session()
    try:
        admin = find_admin_by_email(session, admin_email)
        if not admin:
            print("Admin not found.")
            return

        # Choose trainer
        trainer_email = input("Trainer email: ").strip()
        trainer = find_trainer_by_email(session, trainer_email)
        if not trainer:
            print("Trainer not found.")
            return

        # Choose room
        print("\nAvailable rooms:")
        rooms = session.query(Room).all()
        for r in rooms:
            status = "active" if r.is_active else "inactive"
            print(f"  ID {r.room_id}: {r.room_name} (capacity {r.capacity}, {status})")

        room_id_str = input("Enter room ID: ").strip()
        try:
            room_id = int(room_id_str)
        except ValueError:
            print("Room ID must be an integer.")
            return

        room = session.query(Room).filter_by(room_id=room_id).first()
        if not room:
            print("Room not found.")
            return
        if not room.is_active:
            print("Selected room is not active.")
            return

        class_name = input("Class name: ").strip()
        if not class_name:
            print("Class name is required.")
            return

        description = input("Description (optional): ").strip()
        start_time = parse_datetime("Start datetime")
        if start_time is None:
            return
        end_time = parse_datetime("End datetime")
        if end_time is None:
            return
        if end_time <= start_time:
            print("End time must be after start time.")
            return

        capacity_str = input(f"Capacity (<= room capacity {room.capacity}): ").strip()
        try:
            capacity = int(capacity_str)
        except ValueError:
            print("Capacity must be an integer.")
            return

        if capacity <= 0 or capacity > room.capacity:
            print("Capacity must be between 1 and the room capacity.")
            return

        # Simple room conflict check 
        overlapping_classes = (
            session.query(FitnessClass)
            .filter(
                FitnessClass.room_id == room.room_id,
                FitnessClass.start_time < end_time,
                FitnessClass.end_time > start_time,
                FitnessClass.status != "cancelled",
            )
            .all()
        )
        if overlapping_classes:
            print("\nError: This time overlaps with an existing class in that room:")
            for c in overlapping_classes:
                print(
                    f"  - {c.class_name} from {c.start_time} to {c.end_time} "
                    f"(status: {c.status})"
                )
            return

        new_class = FitnessClass(
            trainer_id=trainer.trainer_id,
            room_id=room.room_id,
            created_by_admin_id=admin.admin_id,
            class_name=class_name,
            description=description or None,
            start_time=start_time,
            end_time=end_time,
            capacity=capacity,
            status="scheduled",
        )

        session.add(new_class)
        session.commit()
        print(
            f"\nClass created successfully with ID {new_class.class_id} "
            f"in room {room.room_name}."
        )

    except Exception as e:
        session.rollback()
        print("Error while creating class / booking room:", e)
    finally:
        session.close()


# Equipment maintenance

def log_equipment_issue():
    # Admin logs a new equipment maintenance issue
    print("\n--- Log Equipment Issue ---")
    admin_email = input("Enter your admin email: ").strip()
    if not admin_email:
        print("Admin email is required.")
        return

    session = get_session()
    try:
        admin = find_admin_by_email(session, admin_email)
        if not admin:
            print("Admin not found.")
            return

        print("\nEquipment list:")
        equipment_list = session.query(Equipment).all()
        if not equipment_list:
            print("No equipment found in the system.")
            return

        for eq in equipment_list:
            room_label = f"Room {eq.room_id}"
            print(
                f"  ID {eq.equipment_id}: {eq.equipment_name} "
                f"({eq.equipment_type or 'type N/A'}) in {room_label} | "
                f"{'OPERATIONAL' if eq.is_operational else 'OUT OF ORDER'}"
            )

        eq_id_str = input("Enter equipment ID: ").strip()
        try:
            eq_id = int(eq_id_str)
        except ValueError:
            print("Equipment ID must be an integer.")
            return

        equipment = session.query(Equipment).filter_by(equipment_id=eq_id).first()
        if not equipment:
            print("Equipment not found.")
            return

        issue_description = input("Describe the issue: ").strip()
        if not issue_description:
            print("Issue description is required.")
            return

        maintenance = EquipmentMaintenance(
            equipment_id=equipment.equipment_id,
            admin_id=admin.admin_id,
            reported_at=datetime.utcnow(),
            status="open",
            issue_description=issue_description,
            resolution_notes=None,
        )

        # Mark equipment as non-operational 
        equipment.is_operational = False

        session.add(maintenance)
        session.commit()
        print(
            f"\nIssue logged with ID {maintenance.maintenance_id} "
            f"for equipment '{equipment.equipment_name}'."
        )

    except Exception as e:
        session.rollback()
        print("Error while logging equipment issue:", e)
    finally:
        session.close()


def update_maintenance_issue():
    # Update status / resolution of an equipment maintenance record
    print("\nUpdate Equipment Maintenance")

    session = get_session()
    try:
        # Show recent/open issues to choose from
        open_issues = (
            session.query(EquipmentMaintenance)
            .order_by(EquipmentMaintenance.reported_at.desc())
            .limit(20)
            .all()
        )

        if not open_issues:
            print("No maintenance records found.")
            return

        print("\nRecent maintenance records:")
        for m in open_issues:
            equipment = m.equipment
            eq_name = equipment.equipment_name if equipment else f"ID {m.equipment_id}"
            print(
                f"  ID {m.maintenance_id}: equipment '{eq_name}', "
                f"status={m.status}, reported_at={m.reported_at}"
            )

        m_id_str = input("\nEnter maintenance ID to update: ").strip()
        try:
            m_id = int(m_id_str)
        except ValueError:
            print("Maintenance ID must be an integer.")
            return

        record = (
            session.query(EquipmentMaintenance)
            .filter_by(maintenance_id=m_id)
            .first()
        )
        if not record:
            print("Maintenance record not found.")
            return

        print(
            f"\nUpdating maintenance record {record.maintenance_id} "
            f"(current status: {record.status})"
        )
        print("Valid statuses: open, in_progress, resolved")
        new_status = input("New status: ").strip().lower()

        if new_status not in ("open", "in_progress", "resolved"):
            print("Invalid status.")
            return

        record.status = new_status

        if new_status == "resolved":
            record.resolved_at = datetime.utcnow()
            notes = input("Resolution notes (optional): ").strip()
            if notes:
                record.resolution_notes = notes

            # If resolved, mark equipment as operational again 
            if record.equipment:
                record.equipment.is_operational = True

        session.commit()
        print("Maintenance record updated successfully.")

    except Exception as e:
        session.rollback()
        print("Error while updating maintenance:", e)
    finally:
        session.close()
