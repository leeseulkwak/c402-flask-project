import requests
from bs4 import BeautifulSoup

# 웹 페이지에 접속하여 HTML 코드 가져오기
url = "http://www.cgv.co.kr/movies/"
response = requests.get(url)
html = response.text

# BeautifulSoup을 사용하여 HTML 코드 파싱
soup = BeautifulSoup(html, "html.parser")

# 필요한 데이터 추출하기
title_tags = soup.select("div.sect-movie-chart strong.title")
img_tags = soup.select("div.sect-movie-chart span.thumb-image > img")
url_tags = soup.select("a.link-reservation")

# 추출한 데이터를 HTML 파일에 저장하기
with open("movie_rank2.html", "w", encoding="utf-8") as file:
    file.write("<html>\n")
    file.write("<head>\n")
    file.write("<title>CGV 영화 순위</title>\n")
    file.write("</head>\n")
    file.write("<body>\n")
    file.write("<h1>CGV 영화 순위</h1>\n")
    file.write("<ul>\n")

    for i in range(len(title_tags)):
        title = title_tags[i].text
        img_src = img_tags[i].attrs["src"]
        url = "http://www.cgv.co.kr" + url_tags[i].attrs["href"]

        file.write("<li>\n")
        file.write(f"<h2>{i+1}위: {title}</h2>\n")
        file.write(f"<img src='{img_src}' alt='{title}'><br>\n")
        file.write(f"<a href='{url}'>예매하기</a>\n")
        file.write("</li>\n")

    file.write("</ul>\n")
    file.write("</body>\n")
    file.write("</html>\n")

print("HTML 파일이 생성되었습니다.")