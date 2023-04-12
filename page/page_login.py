from selenium.webdriver.common.by import By
from util.driver import base, EC, sleep


class PageLogin:
    def __init__(self):
        # self.page = "https://geoserver-sit.starlinkware.com/geoserver/web/"
        self.page = "/geoserver/web/"

        self.locale_switcher = By.XPATH, '//select[@name="localeSwitcher"]'
        self.username = By.ID, 'username'
        self.password = By.ID, 'password'

        self.submit = By.XPATH, '//*[contains(text(), "登录")]'
        self.home = By.XPATH, '//*[contains(text(), "登录身份")]'

    def open_login(self):
        base.base_page(self.page)

    def select_language(self, lan='zh'):
        base.base_select(self.locale_switcher, text=lan)
        sleep(1)

    def input_username(self, username):
        base.base_input(self.username, username)

    def input_password(self, password):
        base.base_input(self.password, password)

    def click_login(self):
        base.base_click(self.submit)

    def check_login(self):
        home = base.base_ec(
            EC.visibility_of_element_located(self.home)
        )

        assert home is not False, '登录失败'

    @staticmethod
    def close_page():
        base.quit()
