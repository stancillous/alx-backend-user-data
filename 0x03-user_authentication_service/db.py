#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base
from user import User
import logging

logging.disable(logging.WARNING)


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Creates and adds a new user to the database.

        Args:
            email (str): The email of the new user.
            hashed_password (str): The hashed password of the new user.

        Returns:
            User: The newly created user object.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user by the provided keyword arguments.

        Args:
            **kwargs (dict): Arbitrary keyword arguments.

        Returns:
            User: The first user found based on the provided keyword arguments.

        Raises:
            NoResultFound: If no user is found.
            InvalidRequestError: If the request is invalid.
        """
        if not kwargs:
            raise InvalidRequestError()
        for keyword, value in kwargs.items():
            if hasattr(User, keyword):
                first_user = self._session.query(User).filter_by(
                    **{keyword: value}).first()
                if first_user is not None:
                    return first_user
                else:
                    raise NoResultFound()
            else:
                raise InvalidRequestError()

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Updates a user with the specified user
        ID using the provided keyword arguments.

        Args:
            user_id (int): The ID of the user to update.
            **kwargs: Arbitrary keyword arguments to update the user with.

        Returns:
            None
        """
        user = self.find_user_by(id=user_id)

        for keyword, value in kwargs.items():
            if hasattr(User, keyword):
                setattr(user, keyword, value)
            else:
                raise ValueError()
        self._session.commit()