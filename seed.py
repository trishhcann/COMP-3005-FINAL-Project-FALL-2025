# seed_data.py
"""
Seed the database with some initial data for testing

Run from project root / where this file live

    source venv/bin/activate   # or your venv command
    python3 seed_data.py
"""

from datetime import datetime, timedelta

from app.db import get_session
from models.member import Member
from models.trainer import Trainer
from models.admin_staff import AdminStaff
from models.room import Room
from models.equipment import Equipment
from models.equipment_maintenance import EquipmentMaintenance
from models.trainer_availability import TrainerAvailability
from models.fitness_goal import FitnessGoal
from models.health_metric import HealthMetric
from models.fitness_class import FitnessClass
from models.class_registration import ClassRegistration
from models.personal_training_session import PersonalTrainingSession


def get_or_create(session, model, defaults=None, **kwargs):
    # helper to avoid duplicate seed rows
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False

    params = dict(kwargs)
    if defaults:
        params.update(defaults)

    instance = model(**params)
    session.add(instance)

    session.flush()

    return instance, True


def seed():
    session = get_session()
    try:
        # Admins 
        admin1, _ = get_or_create(
            session,
            AdminStaff,
            email="admin1@club.com",
            defaults=dict(
                first_name="Alice",
                last_name="Admin",
                password_hash="admin123",   
                role="manager",
            ),
        )

        # Trainers 
        trainer1, _ = get_or_create(
            session,
            Trainer,
            email="trainer1@club.com",
            defaults=dict(
                first_name="Tom",
                last_name="Trainer",
                phone="555-1111",
                specialization="Strength",
                hired_at=datetime(2023, 1, 10).date(),
            ),
        )

        trainer2, _ = get_or_create(
            session,
            Trainer,
            email="trainer2@club.com",
            defaults=dict(
                first_name="Yara",
                last_name="Yoga",
                phone="555-2222",
                specialization="Yoga",
                hired_at=datetime(2023, 5, 1).date(),
            ),
        )

        # Member 
        member1, _ = get_or_create(
            session,
            Member,
            email="member1@club.com",
            defaults=dict(
                first_name="Mia",
                last_name="Member",
                password_hash="member123",
                date_of_birth=datetime(2000, 5, 20).date(),
                gender="F",
                phone="555-3333",
                created_at=datetime.utcnow(),
            ),
        )

        # Rooms 
        room1, _ = get_or_create(
            session,
            Room,
            room_name="Studio A",
            defaults=dict(
                location="1st floor",
                capacity=20,
                is_active=True,
            ),
        )

        room2, _ = get_or_create(
            session,
            Room,
            room_name="Weight Room",
            defaults=dict(
                location="2nd floor",
                capacity=15,
                is_active=True,
            ),
        )

        # Equipment 
        treadmill, _ = get_or_create(
            session,
            Equipment,
            serial_number="TR-1001",
            defaults=dict(
                room_id=room2.room_id,
                equipment_name="Treadmill",
                equipment_type="Cardio",
                is_operational=True,
            ),
        )

        squat_rack, _ = get_or_create(
            session,
            Equipment,
            serial_number="SR-2001",
            defaults=dict(
                room_id=room2.room_id,
                equipment_name="Squat Rack",
                equipment_type="Strength",
                is_operational=True,
            ),
        )

        # Trainer availability, trainer1 available Monday 09:00–12:00
        avail1, _ = get_or_create(
            session,
            TrainerAvailability,
            trainer_id=trainer1.trainer_id,
            day_of_week=1,
            start_time=datetime.strptime("09:00", "%H:%M").time(),
            end_time=datetime.strptime("12:00", "%H:%M").time(),
            defaults=dict(is_recurring=True),
        )

        # Fitness goal for member 
        goal1, _ = get_or_create(
            session,
            FitnessGoal,
            member_id=member1.member_id,
            goal_type="weight_loss",
            status="active",
            defaults=dict(
                target_value=5.0,
                unit="kg",
                start_date=datetime.utcnow().date(),
                target_date=(datetime.utcnow() + timedelta(days=60)).date(),
            ),
        )

        # Health metrics for member, a couple of historical entries
        metric1, _ = get_or_create(
            session,
            HealthMetric,
            member_id=member1.member_id,
            recorded_at=datetime.utcnow() - timedelta(days=7),
            defaults=dict(
                weight=70.0,
                heart_rate=72,
                body_fat_pct=28.0,
                notes="Start of program",
            ),
        )

        metric2, _ = get_or_create(
            session,
            HealthMetric,
            member_id=member1.member_id,
            recorded_at=datetime.utcnow(),
            defaults=dict(
                weight=68.5,
                heart_rate=70,
                body_fat_pct=27.0,
                notes="Week 1 check-in",
            ),
        )

        # Class/room booking
        start_class = datetime.utcnow() + timedelta(days=1)
        end_class = start_class + timedelta(hours=1)

        fitness_class, _ = get_or_create(
            session,
            FitnessClass,
            trainer_id=trainer2.trainer_id,
            room_id=room1.room_id,
            start_time=start_class,
            defaults=dict(
                created_by_admin_id=admin1.admin_id,
                class_name="Morning Yoga",
                description="Gentle vinyasa flow",
                end_time=end_class,
                capacity=15,
                status="scheduled",
            ),
        )

        # Class registration
        reg1, _ = get_or_create(
            session,
            ClassRegistration,
            class_id=fitness_class.class_id,
            member_id=member1.member_id,
            defaults=dict(
                registered_at=datetime.utcnow(),
                attendance_status="registered",
            ),
        )

        # Personal training session 
        pt_start = datetime.utcnow() + timedelta(days=2, hours=2)
        pt_end = pt_start + timedelta(hours=1)

        pt_session, _ = get_or_create(
            session,
            PersonalTrainingSession,
            member_id=member1.member_id,
            trainer_id=trainer1.trainer_id,
            start_time=pt_start,
            defaults=dict(
                room_id=room2.room_id,
                end_time=pt_end,
                status="scheduled",
            ),
        )

        # Equipment maintenance example 
        maintenance1, _ = get_or_create(
            session,
            EquipmentMaintenance,
            equipment_id=treadmill.equipment_id,
            admin_id=admin1.admin_id,
            reported_at=datetime.utcnow() - timedelta(days=1),
            defaults=dict(
                status="open",
                issue_description="Strange noise from motor",
                resolution_notes=None,
            ),
        )

        session.commit()
        print("Seed data inserted (or already existed).")

    except Exception as e:
        session.rollback()
        print("Error while seeding data:", e)
    finally:
        session.close()


if __name__ == "__main__":
    seed()
