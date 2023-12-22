import requests
from bs4 import BeautifulSoup
import webbrowser
import streamlit as st

col_list = st.columns(3)

print.write("# CGV 무비차트")
code = requests.get("http://www.cgv.co.kr/movies/")
soup = BeautifulSoup(code.text, "html.parser")
title = soup.select("div.sect-movie-chart strong.title")
img = soup.select("div.sect-movie-chart span.thumb-image > img")
url_list = soup.select("a.link-reservation")
# 영화 개수에 따라 열의 수를 조정
num_columns = 3  # 한 행에 표시할 영화 수
num_movies = len(title)
rows = (num_movies + num_columns - 1) // num_columns

for row in range(rows):
    cols = st.columns(num_columns)
    for col in range(num_columns):
        index = row * num_columns + col
        if index < num_movies:
            with cols[col]:
                st.image(img[index].attrs["src"], width=200)
                st.write(f"**{index + 1}위** : {title[index].text}")
                if st.button("예매하기", key=index):
                    webbrowser.open("http://www.cgv.co.kr" + url_list[index].attrs["href"])

