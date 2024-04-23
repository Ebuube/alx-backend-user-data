#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoiezed session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str = '', hashed_password: str = '') -> User:
        """Add a user to database
        """
        u = User(email=email, hashed_password=hashed_password)
        self._session.add(u)
        self._session.commit()
        return u

    def find_user_by(self, **kwargs) -> User:
        """
        Filter through database and find the first user with the
        specified attributes and values
        """
        query = self._session.query(User)
        filters = []

        for key, value in kwargs.items():
            if hasattr(User, key):
                filters.append(getattr(User, key) == value)
        try:
            if filters:
                query = query.filter(or_(*filters))
                user = query.first()
                if not user:
                    raise NoResultFound
            else:
                raise InvalidRequestError
            return user
        except NoResultFound:
            raise
        except InvalidRequestError:
            raise
