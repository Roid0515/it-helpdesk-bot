// 챗봇 JavaScript

let conversationState = {
    waitingForRequest: false,
    extractedData: null
};

// DOM 요소
const chatMessages = document.getElementById('chatMessages');
const chatForm = document.getElementById('chatForm');
const messageInput = document.getElementById('messageInput');
const requestModal = document.getElementById('requestModal');
const requestForm = document.getElementById('requestForm');

// 메시지 전송 이벤트
chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const message = messageInput.value.trim();
    
    if (!message) return;
    
    // 사용자 메시지 표시
    addMessage(message, 'user');
    messageInput.value = '';
    
    // 요청 접수 대기 상태인 경우
    if (conversationState.waitingForRequest && conversationState.extractedData) {
        if (confirmRequest(message)) {
            showRequestModal(conversationState.extractedData);
            conversationState.waitingForRequest = false;
            conversationState.extractedData = null;
            return;
        } else {
            addMessage('요청 접수가 취소되었습니다. 다른 도움이 필요하시면 말씀해주세요.', 'bot');
            conversationState.waitingForRequest = false;
            conversationState.extractedData = null;
            return;
        }
    }
    
    // 챗봇 API 호출
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message })
        });
        
        const data = await response.json();
        
        // 봇 응답 표시
        addMessage(data.response, 'bot');
        
        // 요청 접수 의도인 경우
        if (data.intent === 'request' && data.extracted_data) {
            conversationState.waitingForRequest = true;
            conversationState.extractedData = data.extracted_data;
        } else if (data.intent === 'request' && !data.extracted_data) {
            // 요청 접수 모달 표시
            showRequestModal();
        }
        
    } catch (error) {
        console.error('Error:', error);
        addMessage('죄송합니다. 오류가 발생했습니다. 다시 시도해주세요.', 'bot');
    }
});

// 메시지 추가 함수
function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = text;
    
    const timeDiv = document.createElement('div');
    timeDiv.className = 'message-time';
    timeDiv.textContent = getCurrentTime();
    
    messageDiv.appendChild(contentDiv);
    messageDiv.appendChild(timeDiv);
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// 현재 시간 포맷
function getCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' });
}

// 요청 확인 함수
function confirmRequest(message) {
    const confirmKeywords = ['예', 'yes', '네', '확인', '접수', 'ok', '좋아'];
    const messageLower = message.toLowerCase().trim();
    return confirmKeywords.some(keyword => messageLower.includes(keyword));
}

// 요청 모달 표시
function showRequestModal(data = null) {
    if (data) {
        // 추출된 데이터로 폼 채우기
        document.getElementById('userName').value = data.name || '';
        document.getElementById('userDepartment').value = data.department || '';
        document.getElementById('userContact').value = data.contact || '';
        document.getElementById('requestTitle').value = data.title || '';
        document.getElementById('requestContent').value = data.content || '';
    } else {
        // 폼 초기화
        requestForm.reset();
    }
    
    requestModal.classList.add('show');
}

// 요청 모달 닫기
function closeRequestModal() {
    requestModal.classList.remove('show');
    conversationState.waitingForRequest = false;
    conversationState.extractedData = null;
}

// 모달 외부 클릭 시 닫기
requestModal.addEventListener('click', (e) => {
    if (e.target === requestModal) {
        closeRequestModal();
    }
});

// 모달 닫기 버튼
document.querySelector('.close').addEventListener('click', closeRequestModal);

// 요청 접수 폼 제출
requestForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const requestData = {
        user_name: document.getElementById('userName').value.trim(),
        user_department: document.getElementById('userDepartment').value.trim(),
        user_contact: document.getElementById('userContact').value.trim(),
        title: document.getElementById('requestTitle').value.trim(),
        content: document.getElementById('requestContent').value.trim()
    };
    
    try {
        const response = await fetch('/api/submit-request', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            addMessage('요청사항이 성공적으로 접수되었습니다. 감사합니다!', 'bot');
            closeRequestModal();
            requestForm.reset();
        } else {
            addMessage(`접수 중 오류가 발생했습니다: ${data.error}`, 'bot');
        }
        
    } catch (error) {
        console.error('Error:', error);
        addMessage('접수 중 오류가 발생했습니다. 다시 시도해주세요.', 'bot');
    }
});

// Enter 키로 전송 (Shift+Enter는 줄바꿈)
messageInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        chatForm.dispatchEvent(new Event('submit'));
    }
});
