# 실행 파일(.exe) 빌드 가이드

## 방법 1: 배치 파일 사용 (권장)

1. 가상환경 활성화 (이미 되어있다면 생략)
   ```bash
   venv\Scripts\activate
   ```

2. 배치 파일 실행
   ```bash
   build_exe.bat
   ```

3. 빌드 완료 후 `dist` 폴더에서 `ITHelpDeskBot.exe` 확인

## 방법 2: 수동 빌드

1. PyInstaller 설치
   ```bash
   pip install pyinstaller
   ```

2. 빌드 명령어 실행
   ```bash
   pyinstaller --name=ITHelpDeskBot --onefile --windowed --add-data="templates;templates" --add-data="static;static" --hidden-import=flask --hidden-import=flask_sqlalchemy --hidden-import=flask_cors --hidden-import=dotenv --collect-all=flask --collect-all=werkzeug app.py
   ```

3. 빌드 완료 후 `dist` 폴더에서 `ITHelpDeskBot.exe` 확인

## 빌드 옵션 설명

- `--name=ITHelpDeskBot`: 생성될 실행 파일 이름
- `--onefile`: 단일 실행 파일로 생성
- `--windowed`: 콘솔 창 숨기기 (GUI 모드)
- `--add-data`: 템플릿과 정적 파일 포함
- `--hidden-import`: 필요한 모듈 명시적 포함
- `--collect-all`: 특정 패키지의 모든 파일 수집

## 실행 파일 사용 방법

1. `ITHelpDeskBot.exe`를 더블클릭하여 실행
2. 자동으로 브라우저가 열리지 않으면 수동으로 접속:
   - 사용자 챗봇: http://localhost:5000
   - 관리자 게시판: http://localhost:5000/admin

## 주의사항

- 첫 실행 시 Windows Defender가 경고를 표시할 수 있습니다 (서명되지 않은 실행 파일)
- 실행 파일과 같은 폴더에 데이터베이스 파일(`helpdesk.db`)이 생성됩니다
- 실행 파일을 다른 컴퓨터로 옮길 때는 모든 파일을 함께 복사해야 합니다

## 아이콘 추가하기

1. `.ico` 파일을 준비합니다
2. 빌드 명령어에 `--icon=icon.ico` 옵션 추가

## 문제 해결

### 빌드 실패 시
- 가상환경이 활성화되어 있는지 확인
- 모든 패키지가 설치되어 있는지 확인: `pip install -r requirements.txt`

### 실행 파일이 작동하지 않을 때
- 콘솔 창이 보이도록 `--windowed` 대신 `--console` 사용
- 오류 메시지를 확인하여 누락된 모듈 확인
