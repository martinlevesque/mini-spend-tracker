import os
import shutil
from sqlalchemy import create_engine
from sqlalchemy.orm import Session as MakeSession, sessionmaker, scoped_session
from contextlib import contextmanager

project_root = os.path.dirname(os.path.realpath(__file__))

db_env = 'current'

db_filename = os.environ.get('DB_FILENAME', 'spendings.db')
db_folder = os.environ.get('DB_FOLDER', f"{project_root}")

db_location = f"{db_folder}/db/"

db_path = f"{db_location}{db_filename}"

DB_URL = f"sqlite:///{db_path}"

engine = create_engine(DB_URL)

Session = sessionmaker(bind=engine)

session = scoped_session(Session)


@contextmanager
def setup_db(db_id=None):
    print(f"db_id: {db_id}")
    if not db_id:
        db_uri = f"sqlite:///{db_path}"
    else:
        db_uri = f"{db_location}{db_id}.db"

        if not os.path.exists(db_uri):
            # copy the db file

    new_session = MakeSession(create_engine(db_uri))

    try:
        yield new_session
    finally:
        new_session.close()
