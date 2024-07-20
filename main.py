from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests
from time import sleep
import os

url = secret.URL
id = secret.ID
password = secret.PASSWORD
id_xpath = secret.ID_XPATH
pass_xpath = secret.PASS_XPATH
login_xpath = secret.LOGIN_XPATH
line_notify_token = secret.LINE_NOTIFY_TOKEN
calendar_xpath = secret.CALENDAR_XPATH
word_1 = secret.WORD_1
word_2 = secret.WORD_2
word_3 = secret.WORD_3
text1 = secret.TEXT1
text2 = secret.TEXT2
text3 = secret.TEXT3


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
