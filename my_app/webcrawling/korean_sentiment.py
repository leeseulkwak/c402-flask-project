import json
import requests

def get_sentiment(text):
    client_id = "93yd7imx8u"  # client id를 꼭 넣어주세요!
    client_secret = "QahVTyy5WUtBc7DWztsJgl7kj7IedH1r3UrIVG5Q"  # client seceret을 꼭 넣어주세요!
    url = "https://naveropenapi.apigw.ntruss.com/sentiment-analysis/v1/analyze"
    headers = {
        "X-NCP-APIGW-API-KEY-ID": client_id,
        "X-NCP-APIGW-API-KEY": client_secret,
        "Content-Type": "application/json"
    }
    data = {
        "content": text[:min(len(text), 900)]
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    result = json.loads(response.text)
    # print("감성분석 결과 :", result["document"]["sentiment"])
    sentiment = result["document"]["sentiment"]
    confidence = result["document"]["confidence"][sentiment]
    sentiment_ko = {"positive":"긍정", "negative":"부정", "neutral":"중립"}[sentiment]
    return {"result":sentiment_ko, "score":confidence}
