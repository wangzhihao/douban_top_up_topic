#!/usr/bin/env python3
import time, sys
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

# scraper 
driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver')
dummy_message='顶！d=====(￣▽￣*)b'
#driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', service_args=["--verbose", "--log-path=chrome.log"])

def selenium_print(element):
    print(element.get_attribute('outerHTML'))

# scroll to the element by id
def scroll_to_element_by_id(element):
    element_id = element.get_attribute('id')
    driver.execute_script(
        "var testDiv = document.getElementById('"+ element_id + "');"+
        "window.scrollTo(0, testDiv.offsetTop);")

def delete_dummy_comment(topic_url):
    driver.get(topic_url)
    comments = driver.find_elements_by_css_selector("#comments .comment-item")
    dummy_comment = None
    for comment in comments:
        if dummy_message in comment.get_attribute('innerHTML'):
            dummy_comment = comment
            break
    if dummy_comment:
        scroll_to_element_by_id(dummy_comment)
        #show_operations(dummy_comment)
        dummy_comment.click()
        delete_button = dummy_comment.find_element_by_css_selector(".lnk-delete-comment")
        delete_button.click()
        WebDriverWait(driver, 10).until(EC.alert_is_present(), 'Timed out waiting for PA creation confirmation popup to appear.')
        alert = driver.switch_to_alert()
        alert.accept()

def hasCaptcha():
    try:
        driver.find_element_by_css_selector('#captcha_image')
        return True
    except NoSuchElementException:
        return False
def login_douban():
    driver.get("https://www.douban.com/login")
    input_field = driver.find_element_by_css_selector('#email')
    input_field.send_keys("github.topcoder@gmail.com")
    input_field = driver.find_element_by_css_selector('#password')
    input_field.send_keys("12345678QWER")
    send_button = driver.find_element_by_css_selector('input[name="login"]')
    if not hasCaptcha():
        send_button.click()
    else:
        input('waiting user input correct captcha...')
        send_button.click()

def wait_login(url):
    driver.get(url)
    logged_in = False 
    while not logged_in:
        try:
            driver.find_element_by_css_selector('.nav-user-account')
            logged_in = True
        except NoSuchElementException:
            time.sleep(5)
            logged_in = False
#make sure you are already login
def top(topic_url):
    driver.get(topic_url)
    textarea = driver.find_element_by_css_selector('textarea#last')
    textarea.send_keys(dummy_message)
    send_button = driver.find_element_by_css_selector('input[name="submit_btn"]')
    if not hasCaptcha():
        send_button.click()
    else:
        input('waiting user input correct captcha...')
        send_button.click()

login_douban()
top('https://www.douban.com/group/topic/89181794')
top('https://www.douban.com/group/topic/88967583')
top('https://www.douban.com/group/topic/89154773')
driver.quit()
