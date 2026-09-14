import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

# Ejemplo de DATABASE_URL para MySQL:
#   mysql+pymysql://usuario:password@host:3306/nombre_bd
# En local con MySQL instalado en tu PC:
#   mysql+pymysql://root:tu_password@localhost:3306/prende_sql
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:password@localhost:3306/prende_sql")

engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=280)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
