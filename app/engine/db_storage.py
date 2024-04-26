#!/usr/bin/env python
"""
Class for sqlAlchemy that handles __session connections

contains:
    - instance:
        - all: query objects from db
        - new: add objects to db
        - save: commit __session
        - delete: remove __session from db
        - reload: reload the current __session
        - close: end __session

    - attributes:
        - engine
        - __session
        - dic
"""
import os
from app.models.base_model import Base
from dotenv import load_dotenv  # type: ignore
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker, scoped_session
from urllib.parse import quote_plus


load_dotenv()


def db_credentials_are_set():
    required_keys = ["DB_USER", "DB_PASSWORD", "DB_NAME", "DB_HOST", "DB_PORT"]
    return all(os.getenv(key) for key in required_keys)


if not db_credentials_are_set():
    """checks if DB credentials are set in the .env file"""


class DBStorage:
    """
    Handles database operations including connection setup and session management,
    utilizing environment variables for database credentials.
    """

    engine = None
    __session = None

    def __init__(self):
        """Initializes a database engine connection using environment variables"""
        DB_USER = os.getenv("DB_USER")
        DB_PASSOWRD = quote_plus(os.getenv("DB_PASSWORD"))
        DB_HOST = os.getenv("DB_HOST")
        DB_NAME = os.getenv("DB_NAME")
        DB_PORT = os.getenv("DB_PORT")
        DB_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSOWRD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

        try:
            self.engine = create_engine(DB_URL, pool_pre_ping=True)
            # Attempt to connect to the database to verify that the engine is working.
            with self.engine.connect() as conn:
                pass
        except exc.SQLAlchemyError as e:
            print(f"Failed to connect to the database: {e}")
            # manage the error appropriately
            raise

        self.__session = None

    def all(self, cls=None):
        """
        Desc:
            returns a dictionary of all objects(tables)
            in the database
        Return:
            returns a dictionary of __object
        """
        dic = {}
        if cls:
            if type(cls) is str:
                cls = eval(cls)
            query = self.__session.query(cls)
            for elem in query:
                key = f"{type(elem).__name__}.{elem.id}"
                dic[key] = elem
        else:
            # to be completed
            lists = []
            for attr in lists:
                query = self.__session.query(attr)
                for elem in query:
                    key = f"{type(elem).__name__}.{elem.id}"
                    dic[key] = elem
        return dic

    def query_eng(self, cls=None):
        """
        Creates and returns a SQLAlchemy Query object for a specified model class.

        Parameters:
            cls (Base, optional): The model class to query in the database. Must be a subclass of SQLAlchemy's Base.

        Returns:
            Query: A SQLAlchemy Query object configured for the specified model class.
        """
        return self.__session.query(cls)

    def add(self, obj):
        """
        Adds a new object to the session and commits it to the database.

        Parameters:
            obj (Base): An instance of a SQLAlchemy model to be added to the database.

        Raises:
            SQLAlchemyError: If the database operation fails.
        """
        try:
            self.__session.add(obj)
            self.__session.commit()
        except exc.SQLAlchemyError as e:
            self.__session.rollback()
            print(f"Failed to add object to database: {e}")
            raise

    def delete(self, obj):
        """
        Removes an object from the session and the database.

        Parameters:
            obj (Base): An instance of a SQLAlchemy model to be deleted from the database.

        Raises:
            SQLAlchemyError: If the database operation fails.
        """
        try:
            self.__session.delete(obj)
            self.__session.commit()
        except exc.SQLAlchemyError as e:
            self.__session.rollback()
            print(f"Failed to delete object from database: {e}")
            raise

    def update(self, obj):
        """
        Updates an existing object in the session and commits changes to the database.

        Parameters:
            obj (Base): An instance of a SQLAlchemy model that has been modified.

        Raises:
            SQLAlchemyError: If the database operation fails.
        """
        try:
            self.__session.merge(obj)
            self.__session.commit()
        except exc.SQLAlchemyError as e:
            self.__session.rollback()
            print(f"Failed to update object in database: {e}")
            raise

    def find_by_id(self, cls, id):
        """
        Retrieves an object by its ID.

        Parameters:
            cls (Base): The class of the object to retrieve.
            id (int): The primary key of the object in the database.

        Returns:
            instance of cls: The retrieved object, or None if no object found.
        """
        return self.__session.query(cls).get(id)

    def setup_db(self):
        """
        Desc:
             init/load connection
        """
        Base.metadata.create_all(self.engine)
        sec = sessionmaker(bind=self.engine, expire_on_commit=False)
        Session = scoped_session(sec)
        self.__session = Session()

    def save(self):
        """
        Desc:
            commit changes
        """
        self.__session.commit()

    def close(self):
        """
        Desc:
            closes the __session
        """
        self.__session.close()
