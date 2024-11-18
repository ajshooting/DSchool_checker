from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
import requests
from time import sleep
import sys
import os


url = str(os.environ.get("URL"))
id = str(os.environ.get("ID"))
password = str(os.environ.get("PASSWORD"))
id_xpath = str(os.environ.get("ID_XPATH"))
pass_xpath = str(os.environ.get("PASS_XPATH"))
login_xpath = str(os.environ.get("LOGIN_XPATH"))
line_notify_token = str(os.environ.get("LINE_NOTIFY_TOKEN"))
calendar_xpath = str(os.environ.get("CALENDAR_XPATH"))
word_1 = str(os.environ.get("WORD_1"))
word_2 = str(os.environ.get("WORD_2"))
word_3 = str(os.environ.get("WORD_3"))
text1 = str(os.environ.get("TEXT1"))
text2 = str(os.environ.get("TEXT2"))
text3 = str(os.environ.get("TEXT3"))


def main():
    # --- begin program ---
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    # -- login --
    driver.get(url)
    driver.implicitly_wait(5)
    driver.find_element(By.XPATH, id_xpath).send_keys(id)
    driver.find_element(By.XPATH, pass_xpath).send_keys(password)
    driver.find_element(By.XPATH, login_xpath).click()

    # -- get info --
    sleep(1)

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
                    found = True
                    data = {"message": m}
                    requests.post(line_notify_api, headers=headers, data=data)
                # if classes and word2 in classes:
                #     m = text2 + str(row_idx-1) + "日]" + str(col_idx + 8) + "時~"
                # if classes and word3 in classes:
                #     m = text3 + str(row_idx-1) + "日]" + str(col_idx + 8) + "時~"
                #     found = True
        # if found:
        #     print("")
    except:
        print("e?")

    driver.quit()


if __name__ == "__main__":
    for i in range(10):
        try:
            main()
            print("success!", file=sys.stderr)
        except Exception as e:
            print(f"::error ::Error: {e}")  # GitHub Actionsのエラーログに出力
            print(e, file=sys.stderr)  # 標準エラー出力にも表示
            continue
        sleep(60)
