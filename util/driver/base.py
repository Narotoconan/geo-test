from util.driver.main import Driver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.remote.webelement import WebElement
from selenium.common import exceptions
from typing import List
import re

EC = expected_conditions
EX = exceptions


class Base:
    def __init__(self, driver: Driver):
        self.__driver = driver.get_driver()
        self.base_url = 'http://127.0.0.1'

    def quit(self):
        if self.__driver is not None:
            self.__driver.quit()

    def close(self):
        if self.__driver:
            self.__driver.clsoe()
            self.__driver = None

    def base_wait(self, **kwargs) -> WebDriverWait:
        time_out = kwargs.get('time_out', 30)
        poll_frequency = kwargs.get('poll_frequency', 0.5)

        return WebDriverWait(self.__driver, timeout=time_out, poll_frequency=poll_frequency)

    def base_get_element(self, loc: tuple, **kwargs) -> WebElement:
        try:
            return self.base_wait(**kwargs).until(lambda x: x.find_element(*loc))
        except EX.TimeoutException:
            print(f"获取元素失败：{loc}")

    def base_get_elements(self, loc: tuple, **kwargs) -> List[WebElement]:
        try:
            return self.base_wait(**kwargs).until(lambda x: x.find_elements(*loc))
        except EX.TimeoutException:
            print(f"获取元素失败：{loc}")

    def base_ec(self, conditions, method='until', **kwargs):
        if method not in ('until', 'until_not'):
            raise TypeError(f"条件method错误：{method}")
        try:
            return getattr(self.base_wait(**kwargs), method)(conditions)
        except EX.TimeoutException:
            return False

    def base_input(self, loc, txt, is_clear=True, **kwargs):
        ele = self.base_get_element(loc, **kwargs)
        is_clear and ele.clear()
        ele.send_keys(txt)

    def base_click(self, loc: tuple, **kwargs):
        self.base_get_element(loc, **kwargs).click()

    def base_context(self, loc: tuple, **kwargs) -> str:
        return self.base_get_element(loc, **kwargs).text

    def base_select(self, loc: tuple, **kwargs):

        index = kwargs.get('index', None)
        value = kwargs.get('value', None)
        text = kwargs.get('text', None)

        select = Select(self.base_get_element(loc))

        if index is not None:
            select.select_by_index(index)
        elif value is not None:
            select.select_by_value(value)
        elif text is not None:
            select.select_by_visible_text(text)
        else:
            raise TypeError('选择类型，参数缺失（填写 ‘index’或‘value’, ‘text’）')

    def base_page(self, url):
        is_url = re.match(r'https?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url)
        if is_url is None:
            url = self.base_url + url
        self.__driver.get(url)

    def base_script(self, script):
        self.__driver.execute_script(str(script))

    def base_switch_window(self):
        window = self.__driver.window_handles
        print(window)
        self.__driver.switch_to_window(window[-1])
