@echo off
chcp 65001 >nul
echo ================================================
echo IT HelpDesk Bot - 실행 파일 빌드
echo ================================================
echo.

REM 가상환경 활성화
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo 가상환경이 없습니다. 먼저 가상환경을 생성하세요.
    pause
    exit /b 1
)

REM PyInstaller 설치 확인
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller를 설치하는 중...
    pip install pyinstaller
)

echo.
echo 빌드를 시작합니다...
echo.

REM PyInstaller로 빌드
pyinstaller --name=ITHelpDeskBot --onefile --windowed --add-data="templates;templates" --add-data="static;static" --hidden-import=flask --hidden-import=flask_sqlalchemy --hidden-import=flask_cors --hidden-import=dotenv --hidden-import=webbrowser --hidden-import=pymysql --hidden-import=cryptography --hidden-import=sqlalchemy.dialects.mysql.pymysql --collect-all=flask --collect-all=werkzeug --collect-all=jinja2 --collect-all=pymysql app.py

if errorlevel 1 (
    echo.
    echo 빌드 중 오류가 발생했습니다.
    pause
    exit /b 1
)

echo.
echo ================================================
echo 빌드 완료!
echo ================================================
echo dist 폴더에서 ITHelpDeskBot.exe 파일을 확인하세요.
echo.
pause
