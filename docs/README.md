# COMP 3005 Final Project  (01/12)
# Trisha Toocaram, 101267603

## Demo link ## : https://www.youtube.com/watch?v=j-ViYk58uUY

## Description
This system simulates a management application for a fitness club.  
It provides three user roles, each with specific functions:

### **Member**
- Register a new account  
- Update profile  
- Add health metrics (weight, heart rate, body fat %)  
- View a dashboard showing:
  - latest health metric  
  - active fitness goals  
  - classes attended  
  - upcoming personal training sessions  

### **Trainer**
- Set weekly availability (day + start/end time)  
- View their personal training session schedule  

### **Admin Staff**
- View equipment by room  
- Log new equipment maintenance issues  
- Resolve existing issues  

All operations interact with a PostgreSQL database using SQLAlchemy ORM and no raw SQL needed


## Files 
project/
│
├── app/
│ ├── main.py   # Main entry point (menus for each role)
│ ├── db.py     # Database connection + session
│ ├── member_service.py     # Member operations
│ ├── trainer_service.py    # Trainer operations
│ ├── admin_service.py  # Admin operations
│
├── models/
│ ├── base.py   # SQLAlchemy Base
│ ├── member.py     # Member table
│ ├── trainer.py    # Trainer table
│ ├── admin_staff.py    # Admin table
│ ├── room.py   # Room table
│ ├── fitness_goal.py      # Fitness goals
│ ├── health_metric.py      # Health metrics
│ ├── fitness_class.py      # Classes
│ ├── class_registration.py     # Many-to-many registration
│ ├── personal_training_session.py
│ ├── trainer_availability.py
│ ├── equipment.py
│ ├── equipment_maintenance.py
│
├── create_db.py    # Creates all tables from ORM models
├── seed.py    # Sample data for demo
│
├── ERD.pdf     # ER diagram, relational schema + normalization notes
└── README.md



## Execution

### **1. Install Dependencies**
```bash
    pip install sqlalchemy psycopg2-binary
```

### **2. Create the PostgreSQL Database**
In pgAdmin or psql:
```sql
    CREATE DATABASE fitness_club_db;
```
**Note**: Update app/db.py with your PostgreSQL username + password.

### **3. Create the tables
In terminal at the root, (not in /app)
```bash
    python3 create_db.py
```
**Note**: Tables should appear in pgAdmin under fitness_club_db > Schemas > public > Tables

### **4. (Optional but makes things faster) Run Sample Data**
```bash
    python3 seed_data.py
```

### 5. Run the app
```bash
    python3 -m app.main
```



