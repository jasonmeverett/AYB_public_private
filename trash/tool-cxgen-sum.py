from selenium import webdriver
from chromedriver_py import binary_path # this will get you the path variable
svc = webdriver.ChromeService(executable_path=binary_path)
driver = webdriver.Chrome(service=svc)
driver.get("https://cx-case-summarization.ml-c76cb3bd-14c.supportg.n0cg-0zl7.a1.cloudera.site/")
driver.set_window_size(1471, 1025)
driver.find_element(By.ID, "text_input_1").click()
driver.find_element(By.ID, "text_input_1").send_keys("1030260")


from selenium import webdriver
from chromedriver_py import binary_path # this will get you the path variable

svc = webdriver.ChromeService(executable_path=binary_path)
driver = webdriver.Chrome(service=svc)

import re

import mechanicalsoup


# Connect to Google
browser = mechanicalsoup.StatefulBrowser()
browser.open("https://www.google.com/")