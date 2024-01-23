"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError, NoResultFound

from user import Base
from user import User
from typing import TypeVar


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("mysql://ray:raypassword@localhost/alxdb",
                                     echo=False)
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

    def add_user(self, email: str, hashed_password: str) -> TypeVar('User'):
        """method to add a user"""
        new_user = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(new_user)
        session.commit()
        return new_user

    def find_user_by(self, **kwargs):
        """get the first row found in users table"""
        if not kwargs:
            raise InvalidRequestError

        session = self._session
        our_user = session.query(User).filter_by(**kwargs).first()
        if our_user is None:
            raise NoResultFound("Not found")
        return our_user

    def update_user(self, user_id, **kwargs):
        """update user details in db"""
        session = self._session
        try:
            user = self.find_user_by(id=user_id)
            for key, value in kwargs.items():
                if key in user.__dict__:
                    setattr(user, key, value)
                else:
                    raise ValueError
            session.commit()
        except Exception:
            raise ValueError
