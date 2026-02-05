from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

db = SQLAlchemy()


class HelpDeskRequest(db.Model):
    """HelpDesk 요청사항 모델"""
    __tablename__ = 'helpdesk_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), nullable=False)  # 요청자 이름
    user_department = db.Column(db.String(100))  # 부서 (선택사항)
    user_contact = db.Column(db.String(100))  # 연락처 (선택사항)
    title = db.Column(db.String(200), nullable=False)  # 요청 제목
    content = db.Column(db.Text, nullable=False)  # 요청 내용
    category = db.Column(db.String(50))  # 카테고리 (추후 추가)
    status = db.Column(db.String(20), default='pending')  # 상태: pending, processing, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    request_date = db.Column(db.Date, default=date.today)  # 요청일 (일일 접수함 구분용)
    
    def to_dict(self):
        """JSON 직렬화를 위한 딕셔너리 변환"""
        return {
            'id': self.id,
            'user_name': self.user_name,
            'user_department': self.user_department,
            'user_contact': self.user_contact,
            'title': self.title,
            'content': self.content,
            'category': self.category,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'request_date': self.request_date.isoformat() if self.request_date else None
        }


class DailyInbox(db.Model):
    """일일 접수함 모델"""
    __tablename__ = 'daily_inboxes'
    
    id = db.Column(db.Integer, primary_key=True)
    inbox_date = db.Column(db.Date, unique=True, nullable=False)  # 접수함 날짜
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """JSON 직렬화를 위한 딕셔너리 변환"""
        return {
            'id': self.id,
            'inbox_date': self.inbox_date.isoformat() if self.inbox_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
