#!/usr/bin/env python

from .db_storage import DBStorage


def load():
    """
    Context manager to initialize and safely close the database connection.
    """
    db = DBStorage()
    db.setup_db()
    try:
        yield db
    finally:
        db.close()
