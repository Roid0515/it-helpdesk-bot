"""
데이터베이스 초기화 스크립트
"""
from app import app, db

with app.app_context():
    # 모든 테이블 삭제 (주의: 기존 데이터가 있으면 삭제됩니다)
    # db.drop_all()
    
    # 모든 테이블 생성
    db.create_all()
    
    print("데이터베이스가 초기화되었습니다.")
