
import json
import pytest
import requests
import urllib.parse

from utils.log import logger as log
from settings import API_ROOT_ENDPOINT


# Aux functions ################################################

def add_user(**kwargs):
    path = urllib.parse.urljoin(API_ROOT_ENDPOINT, 'users/')
    r = requests.post(
        path,
        json=kwargs
    )
    status = json.loads(r.text)
    return status


# Tests ########################################################


@pytest.mark.parametrize('user_params', [
    {},  # no params
    {'f11': 'b11', 'f12': 'b12'},  # <4 wrong params
    {'f21': 'b21', 'f22': 'b22', 'f23': 'b23', 'f24': 'b24'},  # =4 wrong params
    {
        'f31': 'b31', 'f32': 'b32', 'f33': 'b33', 'f34': 'b34',
        'f35': 'b35'},  # >4 wrong params
    {
        'username': 'u1',
        'email': 'email@email.com',
        'dob': '01.01.2001',
        'address': 'addr',
        'f5': 'b5'  # an additional wrong parameter
    },
    {
        'username': 'u2',
        'email': 'email@email.com',
        'dob': '01.01.2001',
        # 'address': 'addr',  # a missing parameter
    },
])
def test_post_invalid_user(user_params):
    '''
    Test that a 400 is returned when a request is made on /users with invalid
    parameters.
    '''
    status = add_user(**user_params)
    assert status['code'] == 400
    assert status['message'].startswith('Invalid parameters.')


def test_post_valid_user():
    '''
    Test that a 200 is returned when a request is made on /users with valid
    json and that the new user is added.
    '''
    status = add_user(
        username='a12345', email='bar@bar.com',
        dob='01/01/1975', address='Bar location'
    )
    assert status['code'] == 200
    assert status['message'] == 'New user added!'


def test_duplicate_users():
    '''
    Test that a 400 is returned when a request is made on /users with an
    already existing user.
    '''
    add_user(
        username='jumper9876', email='j@jump.com',
        dob='01/01/2001', address='Sea'
    )
    status = add_user(
        username='jumper9876', email='j@jump.com',
        dob='01/01/2001', address='Sea'
    )
    assert status['code'] == 400
    assert status['message'] == 'Duplicate user.'


def test_unicode_characters():
    '''
    Test that a 200 is returned when a post request is made on /users with a
    username with unicode characters.
    '''
    status = add_user(
        username='🇵🇹glw👍🍎🎪', email='j@jump.com',
        dob='01/01/2001', address='Sea'
    )
    assert status['code'] == 200
    assert status['message'] == 'New user added!'


@pytest.mark.parametrize('field_text', ['z', 'z'*10, 'z'*128, ])
def test_username_bounded_length(field_text):
    '''
    Test that a 200 is returned when a post request is made on /users with a
    username length below the maximum allowed, i.e 128 characters and above 0.
    '''
    status = add_user(
        username=field_text, email='j@jump.com',
        dob='01/01/2001', address='Sea'
    )
    assert status['code'] == 200
    assert status['message'] == 'New user added!'


@pytest.mark.parametrize('field_text', ['', 'j'*129, ])
def test_username_unbounded_length(field_text):
    '''
    Test that a 400 is returned when a post request is made on /users with a
    username length that does not respect the specified boundaries 0<len<=128
    '''
    status = add_user(
        username=field_text, email='j@jump.com',
        dob='01/01/2001', address='Sea'
    )
    assert status['code'] == 400
    assert status['message'] == 'Input field out of boundaries.'


@pytest.mark.xfail
def test_sql_inject():
    '''
    '''
    status = add_user(
        username='sql_injection1', email='j@jump.com',
        dob='01/01/2001', address='Sea'
    )
    status = add_user(
        username='sql_injection2', email='j@jump.com',
        dob='01/01/2001', address='Sea'
    )

    sql = r'''2%27%20or%20%271%27%20=%20%271'''
    path = urllib.parse.urljoin(API_ROOT_ENDPOINT, 'users/' + sql)
    r = requests.get(path)
    users = json.loads(r.text)
    assert len(users) <= 1


def test_get_single_user():
    '''
    '''
    status = add_user(
        username='single_user', email='j@jump.com',
        dob='01/01/2001', address='Sea'
    )
    path = urllib.parse.urljoin(API_ROOT_ENDPOINT, 'users/single_user')
    r = requests.get(path)
    user = json.loads(r.text)
    assert user[0]['username'] == 'single_user'


def test_post_get_user():
    '''
    Test that a user is added by checking with a GET request.
    '''
    status = add_user(
        username='kwanza', email='j@jump.com',
        dob='01/01/2001', address='Sea'
    )
    path = urllib.parse.urljoin(API_ROOT_ENDPOINT, 'users/')
    r = requests.get(path)
    users = json.loads(r.text)
    status = False
    for u in users:
        if u['username'] == 'kwanza':
            status = True
    assert status == True, 'User entry is missing'


def test_100_valid_users():
    '''
    Create a number of users and check that they all are submitted correctly.
    '''
    username = 'joao_'
    for i in range(100):
        status = add_user(
            username=username+str(i), email='j@jump.com',
            dob='01/01/2001', address='Sea'
        )
    assert status['code'] == 200
    assert status['message'] == 'New user added!'
