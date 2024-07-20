from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests
from time import sleep
import os

url = secrets.URL
id = secrets.ID
password = secrets.PASSWORD
id_xpath = secrets.ID_XPATH
pass_xpath = secrets.PASS_XPATH
login_xpath = secrets.LOGIN_XPATH
line_notify_token = secrets.LINE_NOTIFY_TOKEN
calendar_xpath = secrets.CALENDAR_XPATH
word_1 = secrets.WORD_1
word_2 = secrets.WORD_2
word_3 = secrets.WORD_3
text1 = secrets.TEXT1
text2 = secrets.TEXT2
text3 = secrets.TEXT3


def login():
    driver.get(url)
    driver.implicitly_wait(5)
    driver.find_element(By.XPATH, id_xpath).send_keys(id)
    driver.find_element(By.XPATH, pass_xpath).send_keys(password)
    driver.find_element(By.XPATH, login_xpath).click()


# --- begin program ---
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

# -- login --
login()

# -- get info --
sleep(1)
driver.implicitly_wait(5)

line_notify_api = "https://notify-api.line.me/api/notify"
headers = {"Authorization": f"Bearer {line_notify_token}"}

try:
    table = driver.find_element(By.XPATH, calendar_xpath)
    rows = table.find_elements(By.TAG_NAME, "tr")
    for row_idx, row in enumerate(rows):
        cells = row.find_elements(By.TAG_NAME, "td")
        for col_idx, cell in enumerate(cells):
            classes = cell.get_attribute("class")
            if classes and word_1 in classes:
                m = text1 + str(row_idx - 1) + "日]" + str(col_idx + 8) + "時~"
                print(m)
                found = True
                data = {"message": m}
                requests.post(line_notify_api, headers=headers, data=data)
            # if classes and word2 in classes:
            #     m = text2 + str(row_idx-1) + "日]" + str(col_idx + 8) + "時~"
            #     print(m)
            # if classes and word3 in classes:
            #     m = text3 + str(row_idx-1) + "日]" + str(col_idx + 8) + "時~"
            #     found = True
    # if found:
    #     print("")
except:
    print("e?")
