from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import dotenv_values
import os
from libcloud.storage.drivers.local import LocalStorageDriver
from sqlalchemy_file.storage import StorageManager

config = dotenv_values(".env")
DB_USERNAME = config['DB_USERNAME']
DB_PASSWORD = config['DB_PASSWORD']
DB_HOST = config['DB_HOST']
DB = config['DB']
# Mysql setup
# SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:3306/{DB}"
# Postgresql
SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:5432/{DB}"

# Configure Storage
os.makedirs("./upload_dir/student_image", 0o777, exist_ok=True)
container = LocalStorageDriver("./upload_dir").get_container("student_image")
StorageManager.add_storage("default", container)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
