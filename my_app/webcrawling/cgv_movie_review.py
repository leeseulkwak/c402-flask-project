from selenium import webdriver
import time
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
import korean_sentiment

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
browser = webdriver.Chrome(options=options)
browser.get("http://www.cgv.co.kr/movies/detail-view/?midx=87554#2")
time.sleep(3)

counts = {} # {위치값1 : 10, 위치값2 : 1, 위치값3 : 4, 위치값4 : 5, ....}
while True:
    ActionChains(browser).key_down(Keys.PAGE_DOWN).perform()
    cur_height = browser.execute_script("return document.documentElement.scrollTop")
    # print(cur_height)
    if cur_height in counts:
        counts[cur_height] += 1
    else:
        counts[cur_height] = 1
        # 어떤 숫자가 100회 나오면중단
    if counts[cur_height] >= 100:
        break

# 댓글 수집
comments = browser.find_elements(By.CSS_SELECTOR, 'div.box-comment')
sentiment_dict = {"매우긍정":0, "긍정":0, "중립":0, "부정":0, "매우부정":0}
for i in comments:
    result = i.text.replace("\n", "").strip()
    print(result)
    sentiment_result = korean_sentiment.get_sentiment(result)
    print(f"감성분석 결과 : {sentiment_result['score']:.2f}% 확률로 {sentiment_result['result']}입니다.")
    if sentiment_result["result"] == "긍정":
        if sentiment_result["score"] >= 80:
            sentiment_dict["매우긍정"] += 1
        else:
            sentiment_dict["긍정"] += 1
    elif sentiment_result["result"] == "부정":
        if sentiment_result["score"] >= 80:
            sentiment_dict["매우부정"] += 1
        else:
            sentiment_dict["부정"] += 1
    else:
        sentiment_dict["중립"] += 1
    print("-----------------------------------------")

from html import escape
# HTML 테이블 시작
html = "<table>\n<tr><th>댓글</th><th>감성분석 결과</th></tr>\n"

for i in comments:
    result = i.text.replace("\n", "").strip()
    sentiment_result = korean_sentiment.get_sentiment(result)
    # 테이블의 각 행 추가
    html += f"<tr><td>{escape(result)}</td><td>{sentiment_result['result']} (확률: {sentiment_result['score']:.2f}%)</td></tr>\n"

# HTML 테이블 종료
html += "</table>"

# HTML 파일 저장
with open("comments.html", "w", encoding="utf-8") as f:
    f.write(html)


browser.close()
