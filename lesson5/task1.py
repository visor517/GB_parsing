from faulthandler import disable
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from pymongo import MongoClient, errors
import time


client = MongoClient('127.0.0.1', 27017)
db = client['my_db']
db_news = db.mails

driver = webdriver.Chrome(executable_path='chromedriver')
driver.implicitly_wait(10)

driver.get('https://mail.ru/')
login = 'study.ai_172'
password = 'NextPassword172#'

login_field = driver.find_element(By.NAME, 'login')
login_field.send_keys(login)
driver.find_element(By.XPATH, "//button[@data-testid='enter-password']").click()
pass_field = driver.find_element(By.NAME, 'password')
pass_field.send_keys(password)
driver.find_element(By.XPATH, "//button[@data-testid='login-to-mail']").click()

# в первую новость
driver.get(driver.find_element(By.XPATH, "//a[contains(@class, 'js-letter-list-item')]").get_attribute('href'))


while True:
    time.sleep(7)

    data = {}
    data['title'] = driver.find_element(By.TAG_NAME, 'h2').text
    data['from'] = driver.find_element(By.CLASS_NAME, 'letter-contact').text
    data['date'] = driver.find_element(By.CLASS_NAME, 'letter__date').text
    #data['content'] = driver.find_element(By.CLASS_NAME, 'letter-body').text

    try:
        if not db_news.find_one({'title': data['title']}, {'date': data['date']}):
            db_news.insert_one(data)
    except errors.DuplicateKeyError:
        pass

    if len(driver.find_elements(By.XPATH, "//span[@title='Следующее' and @disabled]")) > 0:
        break

    actions = ActionChains(driver)
    actions.key_down(Keys.CONTROL).send_keys(Keys.DOWN).key_up(Keys.CONTROL).perform()

    
