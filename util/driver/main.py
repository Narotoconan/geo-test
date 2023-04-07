from selenium import webdriver
from typing import List


class Driver:
    __driver = None

    def __init__(self, options: List[str] = None):
        self.__options = [] if not options else options
        self.__chrome_options = webdriver.ChromeOptions()  # 创建一个配置对象
        for o in self.__options:
            self.__chrome_options.add_argument(o)

    def get_driver(self):
        if self.__driver is None:
            self.__driver = webdriver.Chrome(options=self.__chrome_options)
            self.__driver.set_window_size(1920, 1080)
            # self.__driver.maximize_window()

        return self.__driver
