from util.driver.base import Base
from util.driver.main import Driver
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.common import exceptions
import time

driver = Driver([
    '--headless',
    '--no-sandbox',
    '--disable-gpu'
])

base = Base(driver)
actions = ActionChains(driver)

sleep = time.sleep
EC = expected_conditions
EX = exceptions
