# MariaDB 설정 가이드

이 프로젝트는 MariaDB를 기본 데이터베이스로 사용합니다.

## MariaDB 설치

### Windows

1. **MariaDB 다운로드**
   - https://mariadb.org/download/ 접속
   - Windows용 설치 파일 다운로드
   - 설치 시 root 비밀번호 설정

2. **설치 확인**
   ```bash
   mysql --version
   ```

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install mariadb-server
sudo systemctl start mariadb
sudo systemctl enable mariadb
```

### macOS

```bash
brew install mariadb
brew services start mariadb
```

---

## 데이터베이스 생성

### 1. MariaDB 접속

```bash
mysql -u root -p
```

### 2. 데이터베이스 생성

```sql
CREATE DATABASE helpdesk_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. 사용자 생성 (선택사항, 보안 권장)

```sql
CREATE USER 'helpdesk_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON helpdesk_db.* TO 'helpdesk_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

---

## 환경 변수 설정

### 1. `.env` 파일 생성

프로젝트 루트에 `.env` 파일을 생성하고 다음 내용 추가:

```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here-change-this

# MariaDB 연결 정보
DATABASE_URL=mysql+pymysql://helpdesk_user:your_password@localhost:3306/helpdesk_db

# 또는 root 사용자 사용 시
# DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/helpdesk_db
```

### 2. 연결 문자열 형식

```
mysql+pymysql://[사용자명]:[비밀번호]@[호스트]:[포트]/[데이터베이스명]
```

**예시:**
- 로컬: `mysql+pymysql://root:password@localhost:3306/helpdesk_db`
- 원격: `mysql+pymysql://user:pass@192.168.1.100:3306/helpdesk_db`

---

## 패키지 설치

```bash
pip install -r requirements.txt
```

필요한 패키지:
- `pymysql`: MariaDB/MySQL Python 드라이버
- `cryptography`: 암호화 지원 (pymysql 의존성)

---

## 데이터베이스 초기화

```bash
python init_db.py
```

이 명령어는 다음을 수행합니다:
- 테이블 자동 생성 (`helpdesk_requests`, `daily_inboxes`)
- 기존 테이블이 있으면 건너뜀

---

## 연결 테스트

### Python으로 테스트

```python
from app import app, db
with app.app_context():
    db.create_all()
    print("데이터베이스 연결 성공!")
```

### 서버 실행

```bash
python app.py
```

서버가 정상적으로 시작되면 MariaDB 연결이 성공한 것입니다.

---

## 문제 해결

### 1. 연결 오류: "Access denied"

**원인:** 사용자명/비밀번호 오류 또는 권한 부족

**해결:**
```sql
-- 권한 확인
SHOW GRANTS FOR 'helpdesk_user'@'localhost';

-- 권한 부여
GRANT ALL PRIVILEGES ON helpdesk_db.* TO 'helpdesk_user'@'localhost';
FLUSH PRIVILEGES;
```

### 2. 연결 오류: "Can't connect to MySQL server"

**원인:** MariaDB 서버가 실행되지 않음

**해결:**
```bash
# Windows
net start MySQL

# Linux
sudo systemctl start mariadb

# macOS
brew services start mariadb
```

### 3. 문자 인코딩 문제

**원인:** UTF-8 설정 누락

**해결:**
데이터베이스 생성 시 `CHARACTER SET utf8mb4` 사용 확인:
```sql
CREATE DATABASE helpdesk_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. 포트 충돌

**원인:** 다른 서비스가 3306 포트 사용

**해결:**
- MariaDB 설정 파일에서 포트 변경
- 또는 `.env`에서 포트 번호 변경

---

## 개발 환경에서 SQLite 사용하기

개발/테스트 시 SQLite를 사용하려면 `.env` 파일에서:

```env
DATABASE_URL=sqlite:///helpdesk.db
```

로 변경하면 됩니다. 코드 변경 불필요!

---

## 프로덕션 환경 설정

### 보안 권장사항:

1. **전용 사용자 생성**
   ```sql
   CREATE USER 'helpdesk_prod'@'localhost' IDENTIFIED BY 'strong_password';
   GRANT SELECT, INSERT, UPDATE, DELETE ON helpdesk_db.* TO 'helpdesk_prod'@'localhost';
   ```

2. **환경 변수 보호**
   - `.env` 파일을 `.gitignore`에 포함 (이미 포함됨)
   - 프로덕션 서버에서만 `.env` 파일 관리

3. **연결 풀 설정**
   - `app.py`에 이미 연결 풀 설정 포함됨
   - `pool_pre_ping`: 연결 유지 확인
   - `pool_recycle`: 연결 재사용

---

## 마이그레이션 (SQLite → MariaDB)

기존 SQLite 데이터를 MariaDB로 옮기려면:

```bash
python migrate_to_postgresql.py
```

(스크립트 이름은 PostgreSQL이지만 MariaDB에서도 작동합니다)

---

## 완료!

이제 MariaDB가 설정되었습니다. 서버를 실행하고 테스트해보세요!

```bash
python app.py
```

브라우저에서 http://localhost:5000 접속하여 확인하세요.
