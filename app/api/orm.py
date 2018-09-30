
import os

from sqlalchemy import Column, DateTime, String, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer(), primary_key=True)
    username = Column(String(128))
    email = Column(String(128))
    dob = Column(String(128))
    address = Column(String(128))

    def dump(self):
        return dict(
            [(k, v) for k, v in vars(self).items() if not k.startswith('_')]
        )


def init_db(uri):
    engine = create_engine(uri, convert_unicode=True)
    db_session = scoped_session(sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    ))
    Base.query = db_session.query_property()
    Base.metadata.create_all(bind=engine)
    return db_session, engine
