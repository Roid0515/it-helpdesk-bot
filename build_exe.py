"""
.exe 빌드 스크립트
PyInstaller를 사용하여 실행 파일을 생성합니다.
"""
import PyInstaller.__main__
import os
import shutil

# 빌드 옵션 설정
options = [
    'app.py',  # 메인 파일
    '--name=ITHelpDeskBot',  # 실행 파일 이름
    '--onefile',  # 단일 실행 파일로 생성
    '--windowed',  # 콘솔 창 숨기기 (GUI 모드)
    '--add-data=templates;templates',  # 템플릿 폴더 포함
    '--add-data=static;static',  # 정적 파일 폴더 포함
    '--hidden-import=flask',  # Flask 명시적 포함
    '--hidden-import=flask_sqlalchemy',
    '--hidden-import=flask_cors',
    '--hidden-import=dotenv',
    '--hidden-import=pymysql',  # MariaDB/MySQL 드라이버
    '--hidden-import=cryptography',  # pymysql 의존성
    '--hidden-import=sqlalchemy.dialects.mysql.pymysql',  # SQLAlchemy MySQL 드라이버
    '--collect-all=flask',  # Flask 관련 모든 파일 수집
    '--collect-all=werkzeug',
    '--icon=NONE',  # 아이콘 없음 (추후 아이콘 파일 추가 가능)
]

print("=" * 50)
print("IT HelpDesk Bot - 실행 파일 빌드 시작")
print("=" * 50)

try:
    PyInstaller.__main__.run(options)
    print("\n빌드가 완료되었습니다!")
    print("dist 폴더에서 ITHelpDeskBot.exe 파일을 확인하세요.")
except Exception as e:
    print(f"\n빌드 중 오류가 발생했습니다: {e}")
    print("\n수동 빌드 명령어:")
    print("pyinstaller --name=ITHelpDeskBot --onefile --windowed --add-data=\"templates;templates\" --add-data=\"static;static\" app.py")
