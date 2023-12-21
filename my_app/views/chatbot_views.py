from flask import Blueprint, request, url_for, flash, render_template, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from my_app import db
from my_app.forms import UserCreateForm, UserLoginForm, UserForm
from my_app.models import User, Form
from datetime import datetime

from flask import Flask, request, jsonify, abort
import socket
import json
from flask_cors import CORS

bp=Blueprint('chatbot', __name__, url_prefix='/chatbot')

host="127.0.0.1"
port=5050

app=Flask(__name__)
CORS(app)

@bp.route('/chatbot')
def chatbot():
    return render_template('chatbot/chatbot.html')

# 챗봇 엔진 서버와 통신
def get_answer_from_engine(bottype, query):
    # 챗봇 엔진 서버 연결
    mySocket = socket.socket()
    mySocket.connect((host, port))

    # 챗봇 엔진 질의 요청
    json_data = {
        'Query': query,
        'BotType': bottype
    }
    message = json.dumps(json_data)
    mySocket.send(message.encode())

    # 챗봇 엔진 답변 출력
    data = mySocket.recv(2048).decode()
    # result=convert_ticket_to_link(data)
    ret_data = json.loads(data)
    
    # 챗봇 엔진 서버 연결 소켓 닫기
    mySocket.close()
    return ret_data

# def convert_ticket_to_link(data):
#     if "ticket" in data:
#         return '<a href="{0}">{0}</a>'.format(data)
#     else:
#         return data

# 챗봇 엔진 query 전송 API
@bp.route('query/<bot_type>', methods=['POST'])
def query(bot_type):
    body = request.get_json()

    try:
        if bot_type == 'TEST':
            # 챗봇 API 테스트
            ret = get_answer_from_engine(bottype=bot_type, query=body['query'])
            return  jsonify(ret)
        
        elif bot_type == "KAKAO":
            # 카카오톡 스킬 처리
            return jsonify({"message": "KAKAO response"})

        elif bot_type == "NAVER":
            # 네이버톡톡 Web hook 처리
            return jsonify({"message": "NAVER response"})

        else:
            # 정의되지 않은 bot type인 경우 404 오류
            abort(404)

    except Exception as ex:
        # 오류 발생시 500 오류
        abort(500)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)