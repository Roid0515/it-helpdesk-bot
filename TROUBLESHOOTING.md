# 문제 해결 가이드

## 일반적인 오류 및 해결 방법

### 1. "No module named 'pymysql'" 오류

**증상:**
- .exe 파일 실행 시 `ModuleNotFoundError: No module named 'pymysql'` 오류 발생

**원인:**
- PyInstaller가 `pymysql` 모듈을 실행 파일에 포함하지 않음

**해결 방법:**

1. **build_exe.bat 파일 확인**
   - `--hidden-import=pymysql` 옵션이 포함되어 있는지 확인

2. **재빌드**
   ```bash
   build_exe.bat
   ```

3. **수동으로 hidden import 추가 (필요시)**
   ```bash
   pyinstaller --name=ITHelpDeskBot --onefile --windowed --hidden-import=pymysql --hidden-import=cryptography --hidden-import=sqlalchemy.dialects.mysql.pymysql [기타 옵션] app.py
   ```

---

### 2. 데이터베이스 연결 오류

**증상:**
- "Can't connect to MySQL server" 오류
- "Access denied" 오류

**해결 방법:**

1. **MariaDB 서버 실행 확인**
   ```bash
   # Windows
   net start MySQL
   
   # Linux
   sudo systemctl start mariadb
   ```

2. **환경 변수 확인**
   - `.env` 파일에 올바른 `DATABASE_URL` 설정 확인
   - 형식: `mysql+pymysql://user:password@host:port/database`

3. **데이터베이스 생성 확인**
   ```sql
   CREATE DATABASE helpdesk_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

---

### 3. 템플릿 파일을 찾을 수 없음

**증상:**
- "TemplateNotFound" 오류

**해결 방법:**

1. **빌드 시 템플릿 포함 확인**
   - `build_exe.bat`에 `--add-data="templates;templates"` 옵션 확인

2. **재빌드**
   ```bash
   build_exe.bat
   ```

---

### 4. 정적 파일(CSS/JS)을 찾을 수 없음

**증상:**
- 스타일이 적용되지 않음
- JavaScript 오류

**해결 방법:**

1. **빌드 시 정적 파일 포함 확인**
   - `build_exe.bat`에 `--add-data="static;static"` 옵션 확인

2. **재빌드**
   ```bash
   build_exe.bat
   ```

---

### 5. 실행 파일이 너무 큼

**증상:**
- .exe 파일 크기가 100MB 이상

**원인:**
- 모든 의존성이 포함되어 있음 (정상)

**해결 방법:**
- 이는 정상입니다. Flask와 모든 의존성을 포함하므로 크기가 큽니다.
- 필요시 `--exclude-module` 옵션으로 불필요한 모듈 제외 가능

---

### 6. Windows Defender 경고

**증상:**
- 실행 시 Windows Defender가 차단

**해결 방법:**

1. **Windows Defender 예외 추가**
   - Windows 보안 → 바이러스 및 위협 방지 → 설정 관리
   - 제외 추가 → 파일 또는 폴더 선택

2. **코드 서명 (고급)**
   - 코드 서명 인증서로 서명하면 경고 없음

---

### 7. 포트 5000이 이미 사용 중

**증상:**
- "Address already in use" 오류

**해결 방법:**

1. **포트 사용 확인**
   ```bash
   netstat -ano | findstr :5000
   ```

2. **다른 포트 사용**
   - `app.py`에서 포트 변경:
   ```python
   app.run(debug=debug_mode, host='0.0.0.0', port=5001)
   ```

---

### 8. 브라우저가 자동으로 열리지 않음

**증상:**
- 서버는 실행되지만 브라우저가 열리지 않음

**해결 방법:**

1. **수동 접속**
   - 브라우저에서 `http://localhost:5000` 접속

2. **방화벽 확인**
   - Windows 방화벽에서 Python 허용 확인

---

## 빌드 문제 해결

### 빌드 실패 시 체크리스트

- [ ] 가상환경이 활성화되어 있는가?
- [ ] 모든 패키지가 설치되어 있는가? (`pip install -r requirements.txt`)
- [ ] PyInstaller가 설치되어 있는가?
- [ ] 필요한 파일들이 존재하는가? (templates/, static/)
- [ ] 충분한 디스크 공간이 있는가?

### 깨끗한 재빌드

```bash
# 기존 빌드 파일 삭제
rmdir /s /q build
rmdir /s /q dist

# 재빌드
build_exe.bat
```

---

## 로그 확인

### 디버그 모드로 실행

개발 환경에서:
```bash
python app.py
```

콘솔에 오류 메시지가 표시됩니다.

### .exe 파일 디버그

`build_exe.bat`에서 `--windowed` 대신 `--console` 사용:
```bash
pyinstaller --console [기타 옵션] app.py
```

콘솔 창이 열려 오류 메시지를 확인할 수 있습니다.

---

## 추가 도움말

문제가 계속되면:
1. 오류 메시지 전체 복사
2. GitHub Issues에 등록
3. 로그 파일 첨부 (있는 경우)
