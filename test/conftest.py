
import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import settings as stt
from utils.log import logger as log


# Aux functions ################################################
def setup_chrome_driver():
    chrome_options = ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1420,1080')
    chrome_options.add_argument('--disable-web-security')
    chrome_options.add_argument('--allow-running-insecure-content')
    chrome_options.add_argument('--allow-cross-origin-auth-prompt')

    # enable browser logging
    d = DesiredCapabilities.CHROME
    d['loggingPrefs'] = {'browser': 'ALL'}
    driver = webdriver.Chrome(
        options=chrome_options,
        desired_capabilities=d
    )
    return driver


def setup_firefox_driver():
    options = FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(
        firefox_options=options,
    )


# Hooks ########################################################
def pytest_report_header(config):
    return "Running GLW tests"


# Fixtures #####################################################
@pytest.fixture(scope="function", autouse=True)
def test_info(request):
    sep = '<======================================'
    msg = '<=== Running test: "{}"'.format(request.node.nodeid)
    log.info(msg)

    def test_ofni():
        log.info(sep)
    request.addfinalizer(test_ofni)


@pytest.fixture(scope="session", autouse=True)
def session_info(request):
    sep = '#----------------------#'
    begin_session = '#-- Starting session --#'
    finish_session = '#--- Ending session ---#'
    log.info(sep)
    log.info(begin_session)
    log.info(sep)

    def session_ofni():
        log.info(sep)
        log.info(finish_session)
        log.info(sep)
        time.sleep(5)
    request.addfinalizer(session_ofni)


@pytest.fixture(scope="session")
def driver(request):
    driver_flag = request.config.getoption("--driver")
    dri = None
    if driver_flag == 'Chrome':
        dri = setup_chrome_driver()
    elif driver_flag == 'Firefox':
        dri = setup_firefox_driver()
    else:
        msg = 'Non supported browser driver!'
        log.error(msg)
        pytest.exit(msg)

    dri.implicitly_wait(10)
    dri.get(stt.UI_URL)

    def revird():
        # print javascript console.log() messages
        log.info('Running driver finalizer...')

        log.info(dri.get_log('browser'))
        # dri.close()
        dri.quit()

    request.addfinalizer(revird)

    return dri
