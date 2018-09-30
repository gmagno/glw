
import time

import pytest
import selenium
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.log import logger as log


# Aux functions ################################################

def fillin_field(driver, id_field, entry):
    input_field = driver.find_element_by_id(id_field)
    input_field.clear()
    input_field.send_keys(entry)
    return input_field


def click_button(driver, id_button):
    driver.find_element_by_id(id_button).click()


def check_notification(driver, id_notification, notification):
    try:
        WebDriverWait(driver, 4).until(EC.text_to_be_present_in_element(
            (By.ID, id_notification), notification
        ))
        res = True
        err = ''

    except TimeoutException as ex:
        res = False
        err = "`{}` was not found in element with ID `{}`".format(
            notification, id_notification)
        log.error('TimeoutException: {}'.format(err))

    return res, err

# Tests ########################################################


def test_check_title(driver):
    '''
    Test that the page title is as specified.
    '''
    assert 'glw' in driver.title


@pytest.mark.parametrize('field_id', [
    'mainTitle',
    'inputUsername',
    'inputEmail',
    'inputBirthdate',
    'inputAddress',
    'addButton',
    'tableBody',
    'notification',
    'addUserTitle',
    'usersListTitle',
])
def test_html_tags_exist(driver, field_id):
    '''
    Test that all important DOM elements exist in the page with specified id's.
    '''
    res = True
    msg = ''

    try:
        elem = driver.find_element_by_id(field_id)
    except NoSuchElementException as ex:
        res = False
        msg = ex.msg
        log.error('NoSuchElementException: {}'.format(ex))

    assert res == True, msg


@pytest.mark.parametrize('elem_id,entry', [
    ('inputUsername', 'jack'),
    ('inputEmail', 'jack@email.com'),
    ('inputBirthdate', '01.01.2001'),
    ('inputAddress', '1 Road'),
])
def test_fillin_field(driver, elem_id, entry):
    '''
    Test that all input fields work as expected, i.e text typed in by user is
    sent to the input field and visible.
    '''
    filledin_field = fillin_field(driver, elem_id, entry)
    msg = 'textbox with id `{}` did not contain expected value `{}`.'.format(
        elem_id, entry)
    assert filledin_field.get_attribute('value') == entry, msg


@pytest.mark.parametrize(
    'user,email,dob,addr,notif', [
        (
            'cj1', 'cj1@bayw.com', '01.07.1967',
            '12 Miami Rd', 'Code: 200\nMsg: New user added!'
        ),
        (
            'cj2'*43, 'cj2@bayw.com', '01.07.1967',
            '12 Miami Rd', 'Code: 400\nMsg: Input field out of boundaries.'
        ),
    ]
)
def test_click_button_check_notification1(driver, user, email, dob, addr, notif):
    """
    Test all possible notification messages
    """

    fillin_field(driver, "inputUsername", user)
    fillin_field(driver, "inputEmail", email)
    fillin_field(driver, "inputBirthdate", dob)
    fillin_field(driver, "inputAddress", addr)

    click_button(driver, 'addButton')

    success, err = check_notification(driver, 'notification', notif)

    assert success == True, err


@pytest.mark.xfail
@pytest.mark.parametrize(
    'user,email,dob,addr,notif', [
        (
            'cj3!😀', 'cj3@bayw.com', '01.07.1967',
            '12 Miami Rd', 'Code: 400\nMsg: Invalid username.'
        ),
        (
            'cj4', '@£cj4@bayw.com', '01.07.1967',
            '12 Miami Rd', 'Code: 400\nMsg: Invalid email.'
        ),
        (
            'cj5', '@£cj5@bayw.com', '$1.&7.196%',
            '12 Miami Rd', 'Code: 400\nMsg: Invalid birthdate.'
        ),
        (
            'cj6', 'cj6@bayw.com', '01.07.1967',
            '12 Miami Rd😀', 'Code: 400\nMsg: Invalid address.'
        ),
    ]
)
def test_click_button_check_notification2(driver, user, email, dob, addr, notif):
    """
    Test all possible notification messages. These will fail ue to lack of
    functionality on the server side.
    """

    fillin_field(driver, "inputUsername", user)
    fillin_field(driver, "inputEmail", email)
    fillin_field(driver, "inputBirthdate", dob)
    fillin_field(driver, "inputAddress", addr)

    click_button(driver, 'addButton')

    success, err = check_notification(driver, 'notification', notif)

    assert success == True, err


def test_click_button_check_notification_duplicate(driver):

    fillin_field(driver, 'inputUsername', 'cj1')
    fillin_field(driver, 'inputEmail', 'cj1@bayw.com')
    fillin_field(driver, 'inputBirthdate', '01.07.1967')
    fillin_field(driver, 'inputAddress', '12 Long island Rd')

    click_button(driver, 'addButton')
    click_button(driver, 'addButton')

    success, err = check_notification(
        driver, 'notification', 'Code: 400\nMsg: Duplicate user.')

    assert success == True, err


def test_add_user_check_table(driver):
    '''
    Test that submitting a new user adds a new entry to the users table.
    '''
    res = True
    msg = ''

    newentry = {
        'username': 'jack', 'email': 'jack@mail.com',
        'dob': '01.01.2001', 'addr': '1 Road'
    }

    fillin_field(driver, 'inputEmail', newentry['username'])
    fillin_field(driver, 'inputUsername', newentry['email'])
    fillin_field(driver, 'inputBirthdate', newentry['dob'])
    fillin_field(driver, 'inputAddress', newentry['addr'])

    click_button(driver, 'addButton')
    # driver.find_element_by_id('addButton').click()

    table = driver.find_element_by_id('tableBody')
    table_rows = table.find_elements_by_tag_name('tr')

    try:
        WebDriverWait(driver, 4).until(EC.text_to_be_present_in_element(
            (By.ID, 'tableBody'), newentry['username']
        ))

    except TimeoutException as ex:
        res = False
        msg = ex.msg
        log.error('TimeoutException: {}'.format(ex))

    assert res == True, msg
    for e in newentry.values():
        assert e in table.text, 'Entry {} is missing from table!'.format(e)


@pytest.mark.parametrize(
    'user,notification', [
        ('a'*129, 'Code: 400\nMsg: Input field out of boundaries.'),
        ('', 'Code: 400\nMsg: Input field out of boundaries.'),
    ]
)
def test_invalid_username1(driver, user, notification):
    fillin_field(driver, "inputUsername", user)
    fillin_field(driver, "inputEmail", "foo@mail.com")
    fillin_field(driver, "inputBirthdate", "01.01.1981")
    fillin_field(driver, "inputAddress", "12 Ovaltine drive")

    click_button(driver, 'addButton')

    success, err = check_notification(
        driver, 'notification', notification)

    assert success == True, err


@pytest.mark.xfail
@pytest.mark.parametrize(
    'user,notification', [
        ('$£&', 'Code: 400\nMsg: Invalid username.'),
    ]
)
def test_invalid_username2(driver, user, notification):
    fillin_field(driver, "inputUsername", user)
    fillin_field(driver, "inputEmail", "foo@mail.com")
    fillin_field(driver, "inputBirthdate", "01.01.1981")
    fillin_field(driver, "inputAddress", "12 Ovaltine drive")

    click_button(driver, 'addButton')

    success, err = check_notification(
        driver, 'notification', notification)

    assert success == True, err


@pytest.mark.parametrize(
    'email,notification', [
        ('b'*129, 'Code: 400\nMsg: Input field out of boundaries.'),
        ('', 'Code: 400\nMsg: Input field out of boundaries.'),
    ]
)
def test_invalid_email1(driver, email, notification):
    fillin_field(driver, "inputUsername", "valid username")
    fillin_field(driver, "inputEmail", email)
    fillin_field(driver, "inputBirthdate", "01.01.1981")
    fillin_field(driver, "inputAddress", "12 Ovaltine drive")

    click_button(driver, 'addButton')

    success, err = check_notification(
        driver, 'notification', notification)

    assert success == True, err


@pytest.mark.xfail
@pytest.mark.parametrize(
    'email,notification', [
        ('$£&', 'Code: 400\nMsg: Invalid email.'),
        ('Joe Smith <email@example.com>', 'Code: 400\nMsg: Invalid email.'),
        ('あいうえお@example.com', 'Code: 400\nMsg: Invalid email.'),
        ('email@example', 'Code: 400\nMsg: Invalid email.'),
        ('email@example..com', 'Code: 400\nMsg: Invalid email.'),
        (
            'this\ is"really"not\allowed@example.com',
            'Code: 400\nMsg: Invalid email.'
        ),
    ]
)
def test_invalid_email2(driver, email, notification):
    fillin_field(driver, "inputUsername", "valid username")
    fillin_field(driver, "inputEmail", email)
    fillin_field(driver, "inputBirthdate", "01.01.1981")
    fillin_field(driver, "inputAddress", "12 Ovaltine drive")

    click_button(driver, 'addButton')

    success, err = check_notification(
        driver, 'notification', notification)

    assert success == True, err


@pytest.mark.parametrize(
    'dob,notification', [
        ('', 'Code: 400\nMsg: Input field out of boundaries.'),
    ]
)
def test_invalid_dob1(driver, dob, notification):
    fillin_field(driver, "inputUsername", "joanna")
    fillin_field(driver, "inputEmail", "bar@mail.com")
    fillin_field(driver, "inputBirthdate", dob)
    fillin_field(driver, "inputAddress", "12 Ovaltine drive")

    click_button(driver, 'addButton')

    success, err = check_notification(
        driver, 'notification', notification)

    assert success == True, err


@pytest.mark.xfail
@pytest.mark.parametrize(
    'dob,notification', [
        ('$£&', 'Code: 400\nMsg: Invalid birthdate.'),
        ('12>01>1986', 'Code: 400\nMsg: Invalid birthdate.'),
        ('01/01/90', 'Code: 400\nMsg: Invalid birthdate.'),
    ]
)
def test_invalid_dob2(driver, dob, notification):
    fillin_field(driver, "inputUsername", "joanna")
    fillin_field(driver, "inputEmail", "bar@mail.com")
    fillin_field(driver, "inputBirthdate", dob)
    fillin_field(driver, "inputAddress", "12 Ovaltine drive")

    click_button(driver, 'addButton')

    success, err = check_notification(
        driver, 'notification', notification)

    assert success == True, err


@pytest.mark.parametrize(
    'addr,notification', [
        ('d'*129, 'Code: 400\nMsg: Input field out of boundaries.'),
        ('', 'Code: 400\nMsg: Input field out of boundaries.'),
    ]
)
def test_invalid_address1(driver, addr, notification):
    fillin_field(driver, "inputUsername", "joanna")
    fillin_field(driver, "inputEmail", "bar@mail.com")
    fillin_field(driver, "inputBirthdate", "01/02/1993")
    fillin_field(driver, "inputAddress", addr)

    click_button(driver, 'addButton')

    success, err = check_notification(
        driver, 'notification', notification)

    assert success == True, err


@pytest.mark.xfail
@pytest.mark.parametrize(
    'addr,notification', [
        ('$£&', 'Code: 400\nMsg: Invalid address.'),
    ]
)
def test_invalid_address2(driver, addr, notification):
    fillin_field(driver, "inputUsername", "joanna")
    fillin_field(driver, "inputEmail", "bar@mail.com")
    fillin_field(driver, "inputBirthdate", "01/02/1993")
    fillin_field(driver, "inputAddress", addr)

    click_button(driver, 'addButton')

    success, err = check_notification(
        driver, 'notification', notification)

    assert success == True, err


def test_100_valid_users(driver):

    for i in range(100):
        fillin_field(driver, "inputUsername", "joanna_"+str(i))
        fillin_field(driver, "inputEmail", "bar@mail.com")
        fillin_field(driver, "inputBirthdate", "01/02/1993")
        fillin_field(driver, "inputAddress", "12 Ovaltine drive")

        click_button(driver, 'addButton')

        success, err = check_notification(
            driver, 'notification', 'Code: 200\nMsg: New user added!')

        assert success == True, err
