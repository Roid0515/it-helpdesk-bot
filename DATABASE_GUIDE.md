# 데이터베이스 선택 가이드

현재 프로젝트는 SQLite를 사용하고 있지만, 정식 서비스로 확장할 때는 더 강력한 데이터베이스가 필요합니다.

## 추천 순위

### 1. PostgreSQL (가장 추천) ⭐⭐⭐⭐⭐

**장점:**
- ✅ 오픈소스, 무료
- ✅ 강력한 기능 (Full-text search, JSON 지원, 확장성)
- ✅ 동시성 처리 우수 (다중 사용자 환경에 적합)
- ✅ 트랜잭션 및 ACID 준수
- ✅ SQLAlchemy와 완벽 호환
- ✅ 클라우드 호스팅 용이 (AWS RDS, Heroku Postgres, Supabase 등)

**단점:**
- ❌ 설정이 SQLite보다 복잡
- ❌ 별도 서버 필요

**적합한 경우:**
- 중소규모 ~ 대규모 서비스
- 동시 접속자 다수
- 데이터 무결성 중요
- 향후 확장 계획 있음

**호스팅 옵션:**
- **Supabase** (무료 티어 제공, 추천)
- **Heroku Postgres** (무료 티어 있음)
- **AWS RDS** (유료, 엔터프라이즈급)
- **Railway** (무료 티어 제공)
- **자체 서버** (VPS, 클라우드 인스턴스)

---

### 2. MySQL / MariaDB ⭐⭐⭐⭐

**장점:**
- ✅ 널리 사용됨, 검증된 안정성
- ✅ 성능 우수
- ✅ SQLAlchemy 완벽 지원
- ✅ 클라우드 호스팅 용이

**단점:**
- ❌ PostgreSQL보다 기능 제한적
- ❌ 복잡한 쿼리 성능 상대적으로 낮음

**적합한 경우:**
- 기존 MySQL 인프라 활용
- 단순한 CRUD 위주
- 중소규모 서비스

**호스팅 옵션:**
- **PlanetScale** (무료 티어 제공)
- **AWS RDS MySQL**
- **자체 서버**

---

### 3. SQLite (현재) ⭐⭐

**장점:**
- ✅ 설정 불필요
- ✅ 파일 기반, 간단함
- ✅ 개발/테스트에 적합

**단점:**
- ❌ 동시 쓰기 제한 (1개만)
- ❌ 네트워크 접근 불가
- ❌ 확장성 제한
- ❌ 프로덕션 환경에 부적합

**적합한 경우:**
- 개발/테스트 환경
- 단일 사용자
- 소규모 프로젝트
- 프로토타입

---

## 현재 프로젝트에 추천: PostgreSQL

현재 구조(Flask + SQLAlchemy)에서는 **PostgreSQL**을 가장 추천합니다.

### 이유:
1. **SQLAlchemy 호환성**: 현재 코드 수정 최소화
2. **확장성**: 사용자 증가에 대비
3. **무료 호스팅**: Supabase 등 무료 옵션 풍부
4. **기능**: Full-text search, JSON 등 향후 기능 확장 용이

---

## 마이그레이션 가이드

### 옵션 1: Supabase 사용 (가장 쉬움, 추천)

#### 1. Supabase 계정 생성 및 프로젝트 생성
- https://supabase.com 접속
- 무료 계정 생성
- 새 프로젝트 생성

#### 2. 데이터베이스 연결 정보 확인
Supabase 대시보드 → Settings → Database → Connection string 복사

#### 3. 환경 변수 설정
`.env` 파일에 추가:
```env
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
```

#### 4. PostgreSQL 드라이버 설치
```bash
pip install psycopg2-binary
```

#### 5. requirements.txt 업데이트
```
psycopg2-binary==2.9.9
```

#### 6. 데이터베이스 초기화
```bash
python init_db.py
```

---

### 옵션 2: 자체 PostgreSQL 서버

#### 1. PostgreSQL 설치
**Windows:**
- https://www.postgresql.org/download/windows/
- 설치 시 포트 5432 사용 (기본값)

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

**macOS:**
```bash
brew install postgresql
brew services start postgresql
```

#### 2. 데이터베이스 생성
```bash
# PostgreSQL 접속
psql -U postgres

# 데이터베이스 생성
CREATE DATABASE helpdesk_db;

# 사용자 생성 (선택사항)
CREATE USER helpdesk_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE helpdesk_db TO helpdesk_user;
\q
```

#### 3. 환경 변수 설정
`.env` 파일:
```env
DATABASE_URL=postgresql://helpdesk_user:your_password@localhost:5432/helpdesk_db
```

#### 4. 드라이버 설치 및 초기화
```bash
pip install psycopg2-binary
python init_db.py
```

---

### 옵션 3: Heroku Postgres

#### 1. Heroku 계정 생성 및 앱 생성
```bash
heroku login
heroku create your-app-name
```

#### 2. PostgreSQL 추가
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

#### 3. 환경 변수 자동 설정됨
```bash
heroku config:get DATABASE_URL
```

#### 4. 로컬에서 마이그레이션
```bash
heroku run python init_db.py
```

---

## 코드 변경 사항

현재 코드는 **거의 변경 불필요**합니다! SQLAlchemy가 자동으로 처리합니다.

### 필요한 변경:

1. **requirements.txt에 추가:**
```
psycopg2-binary==2.9.9  # PostgreSQL용
# 또는
pymysql==1.1.0  # MySQL용
```

2. **환경 변수만 변경:**
```env
# SQLite (현재)
DATABASE_URL=sqlite:///helpdesk.db

# PostgreSQL
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# MySQL
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/dbname
```

3. **app.py는 변경 불필요:**
```python
# 현재 코드 그대로 사용 가능
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///helpdesk.db')
```

---

## 데이터 마이그레이션 (SQLite → PostgreSQL)

기존 SQLite 데이터를 PostgreSQL로 옮기는 방법:

### 방법 1: SQLAlchemy 마이그레이션 도구 사용

```bash
# Flask-Migrate 설치
pip install flask-migrate

# 마이그레이션 초기화
flask db init

# 마이그레이션 생성
flask db migrate -m "Initial migration"

# 적용
flask db upgrade
```

### 방법 2: 수동 데이터 이전

```python
# migrate_data.py
from app import app, db
from models import HelpDeskRequest, DailyInbox
import sqlite3

# SQLite에서 데이터 읽기
sqlite_conn = sqlite3.connect('helpdesk.db')
sqlite_cursor = sqlite_conn.cursor()

# PostgreSQL에 데이터 쓰기
with app.app_context():
    # SQLite 데이터 읽기
    sqlite_cursor.execute('SELECT * FROM helpdesk_requests')
    requests = sqlite_cursor.fetchall()
    
    # PostgreSQL에 삽입
    for req in requests:
        new_req = HelpDeskRequest(
            id=req[0],
            user_name=req[1],
            # ... 필드 매핑
        )
        db.session.add(new_req)
    
    db.session.commit()
```

---

## 성능 비교

| 항목 | SQLite | PostgreSQL | MySQL |
|------|--------|------------|-------|
| 동시 읽기 | 좋음 | 매우 좋음 | 매우 좋음 |
| 동시 쓰기 | 제한적 (1개) | 매우 좋음 | 좋음 |
| 확장성 | 낮음 | 높음 | 높음 |
| 프로덕션 적합성 | 낮음 | 높음 | 높음 |
| 설정 복잡도 | 매우 낮음 | 중간 | 중간 |

---

## 최종 추천

**현재 프로젝트에는 PostgreSQL (Supabase) 추천**

1. **무료 호스팅**: Supabase 무료 티어로 시작
2. **코드 변경 최소**: SQLAlchemy 덕분에 거의 변경 불필요
3. **확장성**: 사용자 증가 시에도 안정적
4. **기능**: 향후 검색, 분석 기능 추가 용이

---

## 다음 단계

1. Supabase 계정 생성
2. 프로젝트 생성
3. Connection string 복사
4. `.env` 파일에 `DATABASE_URL` 설정
5. `pip install psycopg2-binary`
6. `python init_db.py` 실행
7. 완료! 🎉
