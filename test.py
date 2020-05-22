from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.common.keys import Keys


class CustomError(Exception):
    pass

driver = webdriver.Remote(command_executor='http://selenium-hub:4444/wd/hub', desired_capabilities=DesiredCapabilities.FIREFOX)

driver.get('https://www.google.com')
driver.implicitly_wait(2)
argument = 'Ofrecido'
count=0
max_tries = 10
while True:
    if argument in driver.page_source:
        print("found")
        break
    if count > max_tries:
        print("not found")
        break
    else:
        count+=1
        time.sleep(1)

screenshot = driver.save_screenshot('test1.png')

driver.quit()

print("Finished test. ")