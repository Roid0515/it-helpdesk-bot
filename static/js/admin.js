// 관리자 페이지 JavaScript

let currentDate = null;
let currentStatus = '';

// 페이지 로드 시 초기화
document.addEventListener('DOMContentLoaded', () => {
    loadStats();
    loadDailyInboxes();
    loadRequests();
    
    // 상태 필터 변경 이벤트
    document.getElementById('statusFilter').addEventListener('change', (e) => {
        currentStatus = e.target.value;
        loadRequests();
    });
});

// 통계 정보 로드
async function loadStats() {
    try {
        const response = await fetch('/api/admin/stats');
        const stats = await response.json();
        
        document.getElementById('statTotal').textContent = stats.total;
        document.getElementById('statPending').textContent = stats.pending;
        document.getElementById('statProcessing').textContent = stats.processing;
        document.getElementById('statCompleted').textContent = stats.completed;
        document.getElementById('statToday').textContent = stats.today;
        
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// 일일 접수함 목록 로드
async function loadDailyInboxes() {
    try {
        const response = await fetch('/api/admin/daily-inboxes');
        const inboxes = await response.json();
        
        const inboxList = document.getElementById('inboxList');
        inboxList.innerHTML = '';
        
        if (inboxes.length === 0) {
            inboxList.innerHTML = '<div class="empty-state"><div class="empty-state-text">접수함이 없습니다</div></div>';
            return;
        }
        
        inboxes.forEach(inbox => {
            const inboxItem = document.createElement('div');
            inboxItem.className = 'inbox-item';
            if (currentDate === inbox.inbox_date) {
                inboxItem.classList.add('active');
            }
            
            const date = new Date(inbox.inbox_date);
            const dateStr = date.toLocaleDateString('ko-KR', { 
                year: 'numeric', 
                month: 'long', 
                day: 'numeric',
                weekday: 'short'
            });
            
            inboxItem.innerHTML = `
                <div class="inbox-date">${dateStr}</div>
                <div class="inbox-count">${inbox.request_count}건</div>
            `;
            
            inboxItem.addEventListener('click', () => {
                // 활성화 상태 변경
                document.querySelectorAll('.inbox-item').forEach(item => {
                    item.classList.remove('active');
                });
                inboxItem.classList.add('active');
                
                // 해당 날짜의 요청사항 로드
                currentDate = inbox.inbox_date;
                loadRequests();
            });
            
            inboxList.appendChild(inboxItem);
        });
        
        // 첫 번째 접수함 자동 선택
        if (inboxes.length > 0 && !currentDate) {
            currentDate = inboxes[0].inbox_date;
            document.querySelectorAll('.inbox-item')[0].classList.add('active');
            loadRequests();
        }
        
    } catch (error) {
        console.error('Error loading inboxes:', error);
    }
}

// 요청사항 목록 로드
async function loadRequests() {
    try {
        let url = '/api/admin/requests?';
        if (currentDate) {
            url += `date=${currentDate}`;
        }
        if (currentStatus) {
            url += currentDate ? `&status=${currentStatus}` : `status=${currentStatus}`;
        }
        
        const response = await fetch(url);
        const requests = await response.json();
        
        const requestsList = document.getElementById('requestsList');
        requestsList.innerHTML = '';
        
        // 제목 업데이트
        const contentTitle = document.getElementById('contentTitle');
        if (currentDate) {
            const date = new Date(currentDate);
            const dateStr = date.toLocaleDateString('ko-KR', { 
                year: 'numeric', 
                month: 'long', 
                day: 'numeric'
            });
            contentTitle.textContent = `${dateStr} 요청사항`;
        } else {
            contentTitle.textContent = '요청사항 목록';
        }
        
        if (requests.length === 0) {
            requestsList.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">📭</div>
                    <div class="empty-state-text">요청사항이 없습니다</div>
                </div>
            `;
            return;
        }
        
        requests.forEach(request => {
            const requestItem = document.createElement('div');
            requestItem.className = 'request-item';
            
            const createdDate = new Date(request.created_at);
            const dateStr = createdDate.toLocaleString('ko-KR');
            
            requestItem.innerHTML = `
                <div class="request-header">
                    <div>
                        <div class="request-title">${escapeHtml(request.title)}</div>
                        <div class="request-meta">
                            <span>👤 ${escapeHtml(request.user_name)}</span>
                            ${request.user_department ? `<span>🏢 ${escapeHtml(request.user_department)}</span>` : ''}
                            ${request.user_contact ? `<span>📞 ${escapeHtml(request.user_contact)}</span>` : ''}
                            <span>🕒 ${dateStr}</span>
                        </div>
                    </div>
                    <span class="request-status ${request.status}">${getStatusText(request.status)}</span>
                </div>
                <div class="request-content">${escapeHtml(request.content)}</div>
            `;
            
            requestItem.addEventListener('click', () => {
                showRequestDetail(request.id);
            });
            
            requestsList.appendChild(requestItem);
        });
        
        // 통계 새로고침
        loadStats();
        
    } catch (error) {
        console.error('Error loading requests:', error);
    }
}

// 요청사항 상세 보기
async function showRequestDetail(requestId) {
    try {
        const response = await fetch(`/api/admin/requests/${requestId}`);
        const request = await response.json();
        
        const detailModal = document.getElementById('detailModal');
        const requestDetail = document.getElementById('requestDetail');
        
        const createdDate = new Date(request.created_at);
        const dateStr = createdDate.toLocaleString('ko-KR');
        
        requestDetail.innerHTML = `
            <div class="detail-section">
                <div class="detail-label">제목</div>
                <div class="detail-value">${escapeHtml(request.title)}</div>
            </div>
            <div class="detail-section">
                <div class="detail-label">요청자 정보</div>
                <div class="detail-value">
                    이름: ${escapeHtml(request.user_name)}<br>
                    ${request.user_department ? `부서: ${escapeHtml(request.user_department)}<br>` : ''}
                    ${request.user_contact ? `연락처: ${escapeHtml(request.user_contact)}` : ''}
                </div>
            </div>
            <div class="detail-section">
                <div class="detail-label">상세 내용</div>
                <div class="detail-value" style="white-space: pre-wrap;">${escapeHtml(request.content)}</div>
            </div>
            <div class="detail-section">
                <div class="detail-label">접수일시</div>
                <div class="detail-value">${dateStr}</div>
            </div>
            <div class="detail-section">
                <div class="detail-label">현재 상태</div>
                <div class="detail-value">
                    <span class="request-status ${request.status}">${getStatusText(request.status)}</span>
                </div>
            </div>
            <div class="detail-actions">
                ${request.status !== 'pending' ? `
                    <button class="btn-status pending" onclick="updateStatus(${request.id}, 'pending')">대기중으로 변경</button>
                ` : ''}
                ${request.status !== 'processing' ? `
                    <button class="btn-status processing" onclick="updateStatus(${request.id}, 'processing')">처리중으로 변경</button>
                ` : ''}
                ${request.status !== 'completed' ? `
                    <button class="btn-status completed" onclick="updateStatus(${request.id}, 'completed')">완료로 변경</button>
                ` : ''}
            </div>
        `;
        
        detailModal.classList.add('show');
        
    } catch (error) {
        console.error('Error loading request detail:', error);
        alert('요청사항을 불러오는 중 오류가 발생했습니다.');
    }
}

// 상태 업데이트
async function updateStatus(requestId, newStatus) {
    try {
        const response = await fetch(`/api/admin/requests/${requestId}/status`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ status: newStatus })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            closeDetailModal();
            loadRequests();
            loadStats();
        } else {
            alert(`상태 업데이트 중 오류가 발생했습니다: ${data.error}`);
        }
        
    } catch (error) {
        console.error('Error updating status:', error);
        alert('상태 업데이트 중 오류가 발생했습니다.');
    }
}

// 상세 모달 닫기
function closeDetailModal() {
    document.getElementById('detailModal').classList.remove('show');
}

// 모달 외부 클릭 시 닫기
document.getElementById('detailModal').addEventListener('click', (e) => {
    if (e.target.id === 'detailModal') {
        closeDetailModal();
    }
});

// 상태 텍스트 변환
function getStatusText(status) {
    const statusMap = {
        'pending': '대기중',
        'processing': '처리중',
        'completed': '완료'
    };
    return statusMap[status] || status;
}

// HTML 이스케이프
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
