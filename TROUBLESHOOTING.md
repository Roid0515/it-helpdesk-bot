# 문제 해결 가이드

## 일반적인 오류 및 해결 방법

### 1. 데이터베이스 연결 오류

**증상:**
- "Can't connect to MySQL server" 오류
- "Access denied" 오류

**해결 방법:**

1. **MariaDB 서버 실행 확인**
   ```bash
   # Windows (서비스 이름은 설치에 따라 다를 수 있음)
   net start MariaDB
   
   # Linux
   sudo systemctl start mariadb
   ```

2. **환경 변수 확인**
   - `.env` 파일에 올바른 `DATABASE_URL` 설정 확인
   - 형식: `mysql+pymysql://user:password@host:port/database`

3. **데이터베이스 생성 확인**
   - DBeaver 또는 `scripts/create_helpdesk_tables.sql`로 `helpdesk_db` 및 테이블 생성

---

### 2. 포트 5000이 이미 사용 중

**증상:**
- "Address already in use" 오류

**해결 방법:**

1. **포트 사용 확인**
   ```bash
   netstat -ano | findstr :5000
   ```

2. **다른 포트 사용**
   - `app.py` 마지막 줄에서 포트 변경:
   ```python
   app.run(debug=True, host='0.0.0.0', port=5001)
   ```

---

### 3. 로그 확인

개발 환경에서 실행 시 콘솔에 오류 메시지가 표시됩니다.

```bash
python app.py
```

문제가 계속되면 오류 메시지 전체를 확인하세요.
