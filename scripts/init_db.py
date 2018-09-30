
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api import orm

engine = create_engine(os.getenv('DB_URL', default='sqlite:///persistent.db'))

orm.Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

users = [
    {
        'username': 'albert', 'email': 'al@bert.com',
        'dob': '01/01/1991', 'address': '1 Ovaltine Drive',
    },
    {
        'username': 'bethanie', 'email': 'be@thanie.com',
        'dob': '02/02/2002', 'address': '02 Astoria Heights'
    },
    {
        'username': 'charles', 'email': 'ch@arles.com',
        'dob': '03/03/3003', 'address': '03 Lamartine Babo'
    },
]

for u in users:
    new_user = orm.User(**u)
    session.add(new_user)
    session.commit()
