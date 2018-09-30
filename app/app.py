
import os
import re

import connexion
from flask_pymongo import PyMongo
from connexion.resolver import RestyResolver
from flask_cors import CORS
from sqlalchemy import text

from api import orm
from utils.log import logger as log


db_session, db_engine = orm.init_db(
    os.getenv('DB_URL', default='sqlite:///persistent.db'))


def get(**kwargs):
    msg = 'Welcome, this is GLW api!\nFor info on available endpoints go to /api/v1/ui'
    return {'code': 200, 'message': msg}, 200


def post_users(**kwargs):
    allowed_params = ['username', 'email', 'dob', 'address']
    user = kwargs['user']
    if len(user) != 4 or set(user.keys()) != set(allowed_params):
        # check for invalid parameters
        ret = {'code': 400, 'message': 'Invalid parameters.'}, 400
    elif (
        any(map(lambda x: len(x) > 128, user.values())) or
        any(map(lambda x: len(x) < 1, user.values()))
    ):
        # check if parameters length respect boundaries
        ret = {'code': 400, 'message': 'Input field out of boundaries.'}, 400
    elif db_session.query(orm.User).filter_by(
        username=user['username']
    ).first() is not None:
        # check for duplicates
        ret = {'code': 400, 'message': 'Duplicate user.'}, 400
    else:
        new_user = orm.User(**kwargs['user'])
        db_session.add(new_user)
        db_session.commit()
        ret = {'code': 200, 'message': 'New user added!'}, 200
    return ret


def get_users(**kwargs):
    q = db_session.query(orm.User)
    q = q.all()
    return [p.dump() for p in q], 200


def get_user(**kwargs):
    '''
    Implementation vulnerable to sql injection,
    e.g r2%27%20or%20%271%27%20=%20%271
    '''
    sql = text(
        """SELECT * fROM users WHERE (username='{}');""".format(kwargs['username']))

    result = db_engine.execute(sql)
    results = []
    for row in result:
        results.append(dict(row))
    return results, 200


app = connexion.FlaskApp(__name__)
CORS(app.app)
application = app.app
application.url_map.strict_slashes = False

app.add_api(
    'glw-api.yml',
    arguments={'title': 'GLW API'},
    resolver=RestyResolver('api'),
    strict_validation=True,
    validate_responses=True,
    swagger_ui=True,  # endpoint: ...<basePath>/ui
    swagger_json=True,  # endpoint: ...<basePath>/swagger.json
)


if __name__ == '__main__':
    log.info('Running GLW api...')
    app.run(
        host='127.0.0.1',
        port=60010,
        debug=True,
    )
