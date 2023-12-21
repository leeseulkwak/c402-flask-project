//클릭일 경우
document.getElementById('submitButton').addEventListener('click', function () {
  submitQuery();
});

// 엔터키 이벤트 리스너 추가
document.getElementById('roomQuery').addEventListener('keypress', function (e) {
  if (e.key === 'Enter') { // 엔터키인 경우
    submitQuery();
  }
});

function submitQuery() {
  var roomQuery = document.getElementById('roomQuery').value.trim();

  if (roomQuery === '') {
    displayResponse('주문 내용을 확인해 주세요 ^-^;;');
    return; // 함수를 여기서 종료시켜 추가적인 처리를 방지
  }


  // 요청 내용 표시
  displayRequest(roomQuery);

  fetch('http://127.0.0.1:5000/chatbot/query/TEST', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ query: roomQuery })
  })
    .then(response => response.json())
    .then(data => {
      console.log(data);
      displayResponse(data.Answer); // 서버 응답을 화면에 표시하는 함수 호출
    })
    .catch(error => console.error('Error:', error));
}

// 서버 응답을 웹 페이지에 표시하는 함수
function displayResponse(data) {
  var responseArea = document.getElementById('serverResponse');
  var responseDiv = document.createElement('div');
  var responseElement = document.createElement('p');
  responseElement.innerHTML = data;
  responseElement.classList.add('message');
  responseElement.classList.add('incoming-message');
  responseArea.appendChild(responseDiv);
  responseDiv.appendChild(responseElement); // 응답 내용을 responseArea에 추가
  updateScroll(); // 스크롤 업데이트
}

// 서버 요청을 웹 페이지에 표시하는 함수
function displayRequest(data) {
  var responseArea = document.getElementById('serverResponse');
  var responseDiv = document.createElement('div');
  var requestElement = document.createElement('p');
  requestElement.innerHTML = data;
  // CSS 클래스를 추가하여 오른쪽 정렬 스타일을 적용합니다.
  responseDiv.classList.add('right-align')
  requestElement.classList.add('message');
  requestElement.classList.add('outgoing-message');
  responseArea.appendChild(responseDiv);
  responseDiv.appendChild(requestElement); // 요청 내용을 responseArea에 추가
  updateScroll(); // 스크롤 업데이트
}

function updateScroll() {
  window.scrollTo({
    top: document.body.scrollHeight,
    behavior: 'smooth'
  });
}

