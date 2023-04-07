import pytest
from page.page_login import PageLogin

page_login = PageLogin()


@pytest.fixture(scope='session', autouse=True)
def login_geoserver():
    page_login.open_login()
    page_login.input_username("admin")
    page_login.input_password("goPOLrxluneiwxgQHxU9rL61Nh8zdOen")

    page_login.click_login()

    try:
        page_login.check_login()
    except AssertionError:
        pytest.exit("登录失败！")

    # yield
    # page_login.close_page()
