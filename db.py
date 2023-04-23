import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

project_root = os.path.dirname(os.path.realpath(__file__))

db_env = 'current'

db_filename = os.environ.get('DB_FILENAME', 'spendings.db')

db_location = f"{project_root}/db/"

db_path = f"{db_location}{db_filename}"


DB_URL = f"sqlite:///{db_path}"

engine = create_engine(DB_URL)

Session = sessionmaker(bind=engine)

session = scoped_session(Session)
