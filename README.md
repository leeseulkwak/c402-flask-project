
기술 : python, html, javascript, css, sqlgate
간단 설명

-. 영화 리뷰 게시판 [flask_app이용]
-. navbar
 1) 회원가입
 2) 로그인
 3) 리뷰게시판
    -. 작성자 외 게시글 및 답변 수정/삭제 불가
    -. 게시글 답변 갯수 표출
    -. 게시글 및 답변 추천 기능
    -. 게시글 찾기 기능
    -. 게시글 번호 처리 기능
    -. 게시글 최대 표출 화면 초과시 다음 페이징 처리 기능

-. index
 1) 챗봇예약하기[bot.py엔진 서버는 항상 On상태되어야함)
    : 챗봇엔진으로 채팅 질문을 분류해서 답변하는 채팅 기능
    * 동작 방법 (질문이 추가 될때 마다 반복 작업)
      (1) train_data.xlsx에 신규 질문 및 답변 기능 작업해서 DB에 넣어 줌
          -> chatbot_data_excel.py 실행해서 자동 DB 업데이트 가능
      (2) total_train_data.csv를 통해서 질문과 의도 숫자를 넣어줌
      (3) train_model.py를 재생성
      (4) ner_train.txt에서 전처리 진행(품사 구분)
      (5) train_model.py를 재생성
      
 2) 상위 영화 리스트 (셀레니움으로 웹스크래핑한 정보를 표출해줌)
