from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.common.keys import Keys


class CustomError(Exception):
    pass

# driver = webdriver.Remote(command_executor='http://selenium-hub:4444/wd/hub', desired_capabilities=DesiredCapabilities.FIREFOX)

driver.get('https://www.google.com')
driver.implicitly_wait(5)

try:
    input_object = driver.find_element_by_name('q')
    input_object.send_keys('les fucking gooooo')
except Exception as e:
    print(e)
    print("an error ocurred")

screenshot = driver.save_screenshot('test1.png')

driver.quit()

print("Finished test. ")