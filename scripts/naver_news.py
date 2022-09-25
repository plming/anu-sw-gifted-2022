from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv


if __name__ == '__main__':
    """
    사용법: url 변수를 네이버 뉴스 댓글 url로 변경 후 실행
    """
    url = 'https://n.news.naver.com/article/comment/005/0001509941'

    driver = webdriver.Chrome('chromedriver')
    driver.implicitly_wait(time_to_wait=5)

    driver.get(url)

    while True:
        try:
            more = driver.find_element(By.CSS_SELECTOR, 'a.u_cbox_btn_more')
            more.click()

            DELAY_TIME = 0.1
            time.sleep(DELAY_TIME)

        except:
            break

    elements = driver.find_elements(By.CSS_SELECTOR, 'span.u_cbox_contents')
    comments = [content.text for content in elements]
    driver.quit()

    rows = list(zip(comments))

    file_name = "recrawled.csv"
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)
