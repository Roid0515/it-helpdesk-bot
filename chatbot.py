"""
챗봇 로직 모듈
사용자와의 대화를 처리하고 요청사항을 파싱합니다.
"""

import re
from datetime import datetime


class ChatBot:
    """HelpDesk 챗봇 클래스"""
    
    def __init__(self):
        # 간단한 안내사항 데이터베이스 (추후 확장 가능)
        self.faq = {
            '비밀번호': '비밀번호 재설정은 IT팀으로 문의해주세요. (내선: 1234)',
            '프린터': '프린터 문제는 IT팀으로 문의해주세요. (내선: 1234)',
            '네트워크': '네트워크 문제 발생 시 IT팀으로 즉시 연락해주세요. (내선: 1234)',
            '소프트웨어': '소프트웨어 설치 요청은 IT팀으로 문의해주세요. (내선: 1234)',
            '하드웨어': '하드웨어 문제는 IT팀으로 문의해주세요. (내선: 1234)',
        }
        
        # 인사말 패턴
        self.greetings = ['안녕', '하이', 'hello', 'hi', '반가워', '처음']
        
    def process_message(self, message, conversation_history=None):
        """
        사용자 메시지를 처리하고 응답을 생성합니다.
        
        Args:
            message: 사용자 입력 메시지
            conversation_history: 대화 이력 (선택사항)
            
        Returns:
            dict: {
                'response': 응답 메시지,
                'intent': 의도 (greeting, faq, request, unknown),
                'extracted_data': 추출된 데이터 (요청사항인 경우)
            }
        """
        message_lower = message.lower().strip()
        
        # 1. 인사말 확인
        if any(greeting in message_lower for greeting in self.greetings):
            return {
                'response': '안녕하세요! IT HelpDesk 챗봇입니다. 무엇을 도와드릴까요?\n\n- 업무 요청을 접수하려면 "요청" 또는 "접수"라고 말씀해주세요.\n- 간단한 안내사항을 확인하려면 키워드를 입력해주세요.',
                'intent': 'greeting',
                'extracted_data': None
            }
        
        # 2. 요청 접수 의도 확인
        request_keywords = ['요청', '접수', '문의', '도움', '문제', '에러', '오류', '해결']
        if any(keyword in message for keyword in request_keywords):
            return {
                'response': '요청사항을 접수해드리겠습니다. 다음 정보를 알려주세요:\n\n1. 이름\n2. 부서 (선택사항)\n3. 연락처 (선택사항)\n4. 요청 제목\n5. 상세 내용\n\n예시: "홍길동, 개발팀, 010-1234-5678, 프린터 연결 문제, 프린터가 인식이 안됩니다"',
                'intent': 'request',
                'extracted_data': None
            }
        
        # 3. FAQ 확인
        for keyword, answer in self.faq.items():
            if keyword in message:
                return {
                    'response': answer,
                    'intent': 'faq',
                    'extracted_data': None
                }
        
        # 4. 요청사항 데이터 추출 시도 (이름, 제목, 내용 등이 포함된 경우)
        extracted = self._extract_request_data(message)
        if extracted:
            return {
                'response': f'요청사항을 확인했습니다:\n\n이름: {extracted.get("name", "미입력")}\n부서: {extracted.get("department", "미입력")}\n연락처: {extracted.get("contact", "미입력")}\n제목: {extracted.get("title", "미입력")}\n내용: {extracted.get("content", "미입력")}\n\n접수하시겠습니까? (예/아니오)',
                'intent': 'request',
                'extracted_data': extracted
            }
        
        # 5. 기본 응답
        return {
            'response': '죄송합니다. 이해하지 못했습니다. 다시 말씀해주시거나, "요청"이라고 입력하시면 요청 접수를 도와드리겠습니다.',
            'intent': 'unknown',
            'extracted_data': None
        }
    
    def _extract_request_data(self, message):
        """
        메시지에서 요청사항 데이터를 추출합니다.
        간단한 패턴 매칭을 사용합니다. (추후 NLP로 개선 가능)
        """
        # 쉼표로 구분된 정보 추출 시도
        parts = [p.strip() for p in message.split(',')]
        
        if len(parts) >= 3:
            data = {
                'name': parts[0] if len(parts) > 0 else '',
                'department': parts[1] if len(parts) > 1 else '',
                'contact': parts[2] if len(parts) > 2 else '',
                'title': parts[3] if len(parts) > 3 else parts[0] if len(parts) > 0 else '',
                'content': ', '.join(parts[4:]) if len(parts) > 4 else parts[-1] if len(parts) > 0 else message
            }
            return data
        
        # 전화번호 패턴 찾기
        phone_pattern = r'(\d{2,3}-\d{3,4}-\d{4})'
        phone_match = re.search(phone_pattern, message)
        
        # 이름 패턴 (한글 2-4자)
        name_pattern = r'([가-힣]{2,4})'
        name_match = re.search(name_pattern, message)
        
        if name_match or phone_match:
            data = {
                'name': name_match.group(1) if name_match else '',
                'contact': phone_match.group(1) if phone_match else '',
                'title': message[:50] if len(message) > 50 else message,
                'content': message
            }
            return data
        
        return None
    
    def confirm_request(self, message):
        """요청 확인 응답 처리"""
        confirm_keywords = ['예', 'yes', '네', '확인', '접수', 'ok', '좋아']
        message_lower = message.lower().strip()
        
        return any(keyword in message_lower for keyword in confirm_keywords)
