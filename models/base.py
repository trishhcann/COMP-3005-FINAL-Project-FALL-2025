# models/base.py
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# change these to your actual Postgres credentials/database name
# here password: postgres
# database name: fitness_club_db
DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/fitness_club_db"

Base = declarative_base()

engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(bind=engine)
