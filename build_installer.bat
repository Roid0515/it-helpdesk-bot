@echo off
chcp 65001 >nul
echo ================================================
echo IT HelpDesk Bot - 설치 프로그램 빌드
echo ================================================
echo.

REM 1. 먼저 .exe 파일 빌드
echo [1/3] 실행 파일(.exe) 빌드 중...
call build_exe.bat
if errorlevel 1 (
    echo.
    echo 오류: 실행 파일 빌드에 실패했습니다.
    pause
    exit /b 1
)

echo.
echo [2/3] Inno Setup 확인 중...

REM Inno Setup 설치 확인
set INNO_SETUP_PATH=
if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    set INNO_SETUP_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe
) else if exist "C:\Program Files\Inno Setup 6\ISCC.exe" (
    set INNO_SETUP_PATH=C:\Program Files\Inno Setup 6\ISCC.exe
) else (
    echo.
    echo ================================================
    echo Inno Setup이 설치되어 있지 않습니다!
    echo ================================================
    echo.
    echo Inno Setup을 설치해야 합니다:
    echo 1. https://jrsoftware.org/isdl.php 접속
    echo 2. Inno Setup 6 다운로드 및 설치
    echo 3. 설치 후 이 스크립트를 다시 실행하세요.
    echo.
    pause
    exit /b 1
)

echo Inno Setup 발견: %INNO_SETUP_PATH%
echo.

REM installer 폴더 생성
if not exist "installer" mkdir installer

echo [3/3] 설치 프로그램 빌드 중...
"%INNO_SETUP_PATH%" "setup_script.iss"

if errorlevel 1 (
    echo.
    echo 오류: 설치 프로그램 빌드에 실패했습니다.
    pause
    exit /b 1
)

echo.
echo ================================================
echo 빌드 완료!
echo ================================================
echo.
echo 설치 프로그램 위치: installer\ITHelpDeskBot_Setup.exe
echo.
echo 이 파일을 배포하여 사용자들이 설치할 수 있습니다.
echo.
pause
