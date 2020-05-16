from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

driver = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub', desired_capabilities=DesiredCapabilities.CHROME)

driver.get('https://www.reddit.com')
screenshot = driver.save_screenshot('test1.png')
driver.quit()