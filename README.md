# IT HelpDesk Bot

회사 IT 전산관리자를 위한 HelpDesk 업무 요청 관리 시스템

## 주요 기능

### 사용자(직원) 기능
- 챗봇을 통한 HelpDesk 업무 요청 접수
- 간단한 안내사항 조회

### 관리자 기능
- 일일단위 요청사항 접수함 확인
- 요청사항 상세 조회 및 관리

## 설치 및 실행

### 1. 가상환경 생성 및 활성화
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 2. 패키지 설치
```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정
`.env` 파일을 생성하고 필요한 설정을 추가하세요.

### 4. 데이터베이스 초기화
```bash
python init_db.py
```

### 5. 서버 실행
```bash
python app.py
```

서버가 실행되면:
- 사용자 챗봇: http://localhost:5000
- 관리자 게시판: http://localhost:5000/admin

## 실행 파일(.exe) 빌드

### 간단한 방법 (배치 파일 사용)
```bash
build_exe.bat
```

빌드 완료 후 `dist` 폴더에서 `ITHelpDeskBot.exe` 파일을 확인하세요.

자세한 빌드 방법은 `BUILD_INSTRUCTIONS.md` 파일을 참고하세요.

## 프로젝트 구조

```
IT HelpDesk Bot_260205/
├── app.py                 # Flask 메인 애플리케이션
├── models.py              # 데이터베이스 모델
├── chatbot.py             # 챗봇 로직
├── init_db.py             # 데이터베이스 초기화
├── requirements.txt       # Python 패키지 의존성
├── build_exe.bat          # .exe 빌드 배치 파일
├── BUILD_INSTRUCTIONS.md  # 빌드 가이드
├── .env                   # 환경 변수 (생성 필요)
├── static/                # 정적 파일
│   ├── css/
│   └── js/
└── templates/             # HTML 템플릿
    ├── index.html         # 사용자 챗봇 페이지
    └── admin.html         # 관리자 게시판 페이지
```
