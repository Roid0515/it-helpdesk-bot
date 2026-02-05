"""
SQLite에서 MariaDB/PostgreSQL로 데이터 마이그레이션 스크립트
사용법: python migrate_to_postgresql.py

지원 데이터베이스:
- MariaDB/MySQL
- PostgreSQL
- 기타 SQLAlchemy 지원 데이터베이스
"""
import os
import sqlite3
from dotenv import load_dotenv
from app import app, db
from models import HelpDeskRequest, DailyInbox
from datetime import datetime

load_dotenv()

def migrate_sqlite_to_postgresql():
    """SQLite 데이터를 PostgreSQL로 마이그레이션"""
    
    sqlite_db_path = 'helpdesk.db'
    
    if not os.path.exists(sqlite_db_path):
        print(f"SQLite 데이터베이스 파일을 찾을 수 없습니다: {sqlite_db_path}")
        return
    
    # SQLite 연결
    sqlite_conn = sqlite3.connect(sqlite_db_path)
    sqlite_cursor = sqlite_conn.cursor()
    
    with app.app_context():
        try:
            # 기존 데이터 확인
            sqlite_cursor.execute('SELECT COUNT(*) FROM helpdesk_requests')
            request_count = sqlite_cursor.fetchone()[0]
            
            sqlite_cursor.execute('SELECT COUNT(*) FROM daily_inboxes')
            inbox_count = sqlite_cursor.fetchone()[0]
            
            print(f"마이그레이션할 데이터:")
            print(f"  - 요청사항: {request_count}건")
            print(f"  - 일일 접수함: {inbox_count}건")
            
            if request_count == 0 and inbox_count == 0:
                print("마이그레이션할 데이터가 없습니다.")
                return
            
            # 사용자 확인
            confirm = input("\n마이그레이션을 진행하시겠습니까? (yes/no): ")
            if confirm.lower() != 'yes':
                print("마이그레이션이 취소되었습니다.")
                return
            
            # 요청사항 마이그레이션
            print("\n요청사항 마이그레이션 중...")
            sqlite_cursor.execute('''
                SELECT id, user_name, user_department, user_contact, title, 
                       content, category, status, created_at, request_date
                FROM helpdesk_requests
                ORDER BY id
            ''')
            
            requests = sqlite_cursor.fetchall()
            migrated_requests = 0
            
            for req in requests:
                # 이미 존재하는지 확인
                existing = HelpDeskRequest.query.get(req[0])
                if existing:
                    print(f"  요청사항 ID {req[0]}는 이미 존재합니다. 건너뜁니다.")
                    continue
                
                # 날짜 변환
                created_at = None
                if req[8]:
                    if isinstance(req[8], str):
                        created_at = datetime.fromisoformat(req[8].replace('Z', '+00:00'))
                    else:
                        created_at = datetime.fromtimestamp(req[8])
                
                request_date = None
                if req[9]:
                    if isinstance(req[9], str):
                        request_date = datetime.strptime(req[9], '%Y-%m-%d').date()
                    else:
                        request_date = datetime.fromtimestamp(req[9]).date()
                
                new_request = HelpDeskRequest(
                    id=req[0],
                    user_name=req[1] or '익명',
                    user_department=req[2],
                    user_contact=req[3],
                    title=req[4] or '제목 없음',
                    content=req[5] or '',
                    category=req[6],
                    status=req[7] or 'pending',
                    created_at=created_at,
                    request_date=request_date
                )
                
                db.session.add(new_request)
                migrated_requests += 1
            
            # 일일 접수함 마이그레이션
            print("\n일일 접수함 마이그레이션 중...")
            sqlite_cursor.execute('''
                SELECT id, inbox_date, created_at
                FROM daily_inboxes
                ORDER BY id
            ''')
            
            inboxes = sqlite_cursor.fetchall()
            migrated_inboxes = 0
            
            for inbox in inboxes:
                # 이미 존재하는지 확인
                existing = DailyInbox.query.get(inbox[0])
                if existing:
                    print(f"  접수함 ID {inbox[0]}는 이미 존재합니다. 건너뜁니다.")
                    continue
                
                # 날짜 변환
                inbox_date = None
                if inbox[1]:
                    if isinstance(inbox[1], str):
                        inbox_date = datetime.strptime(inbox[1], '%Y-%m-%d').date()
                    else:
                        inbox_date = datetime.fromtimestamp(inbox[1]).date()
                
                created_at = None
                if inbox[2]:
                    if isinstance(inbox[2], str):
                        created_at = datetime.fromisoformat(inbox[2].replace('Z', '+00:00'))
                    else:
                        created_at = datetime.fromtimestamp(inbox[2])
                
                new_inbox = DailyInbox(
                    id=inbox[0],
                    inbox_date=inbox_date,
                    created_at=created_at
                )
                
                db.session.add(new_inbox)
                migrated_inboxes += 1
            
            # 커밋
            db.session.commit()
            
            print(f"\n✅ 마이그레이션 완료!")
            print(f"  - 요청사항: {migrated_requests}건")
            print(f"  - 일일 접수함: {migrated_inboxes}건")
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ 마이그레이션 중 오류 발생: {str(e)}")
            import traceback
            traceback.print_exc()
        
        finally:
            sqlite_conn.close()


if __name__ == '__main__':
    print("=" * 60)
    print("SQLite → PostgreSQL 데이터 마이그레이션")
    print("=" * 60)
    print("\n주의: 이 스크립트는 SQLite 데이터를 PostgreSQL로 복사합니다.")
    print("PostgreSQL 데이터베이스가 이미 설정되어 있어야 합니다.")
    print("환경 변수 DATABASE_URL이 PostgreSQL을 가리키는지 확인하세요.\n")
    
    migrate_sqlite_to_postgresql()
