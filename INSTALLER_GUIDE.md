# 설치 프로그램 빌드 가이드

IT HelpDesk Bot을 Windows 설치 프로그램(.exe)으로 빌드하는 방법입니다.

## 필요한 도구

### 1. Inno Setup (무료)

**다운로드:**
- 공식 사이트: https://jrsoftware.org/isdl.php
- 버전: Inno Setup 6 (최신 버전)
- 라이선스: 무료 오픈소스

**설치:**
1. 다운로드한 설치 파일 실행
2. 기본 설정으로 설치 진행
3. 설치 경로 확인:
   - 기본: `C:\Program Files (x86)\Inno Setup 6\`
   - 또는: `C:\Program Files\Inno Setup 6\`

---

## 빌드 방법

### 방법 1: 자동 빌드 (권장)

```bash
build_installer.bat
```

이 스크립트는 다음을 자동으로 수행합니다:
1. 실행 파일(.exe) 빌드
2. Inno Setup 확인
3. 설치 프로그램 빌드

**결과물:**
- `installer\ITHelpDeskBot_Setup.exe` - 설치 프로그램

---

### 방법 2: 수동 빌드

#### 1단계: 실행 파일 빌드
```bash
build_exe.bat
```

#### 2단계: Inno Setup 실행
1. Inno Setup Compiler 실행
2. `setup_script.iss` 파일 열기
3. "Build" → "Compile" 클릭

**결과물:**
- `installer\ITHelpDeskBot_Setup.exe`

---

## 설치 프로그램 기능

### 포함된 내용:
- ✅ 실행 파일 (ITHelpDeskBot.exe)
- ✅ README 문서
- ✅ 데이터베이스 설정 가이드
- ✅ 시작 메뉴 바로가기
- ✅ 바탕화면 바로가기 (선택사항)
- ✅ 제거 프로그램

### 설치 위치:
- 기본: `C:\Program Files\IT HelpDesk Bot\`
- 사용자 지정 가능

### 설치 과정:
1. 설치 경로 선택
2. 바로가기 생성 선택
3. 설치 진행
4. 설치 완료 후 자동 실행 (선택사항)

---

## 설치 프로그램 사용자 가이드

### 설치 방법:

1. **설치 프로그램 실행**
   - `ITHelpDeskBot_Setup.exe` 더블클릭

2. **설치 마법사 따라하기**
   - 설치 경로 선택 (기본값 사용 권장)
   - 바로가기 생성 선택
   - "설치" 클릭

3. **설치 완료**
   - 시작 메뉴에서 "IT HelpDesk Bot" 실행
   - 또는 바탕화면 바로가기 사용

### 프로그램 제거:

1. **제어판** → **프로그램 제거**
2. "IT HelpDesk Bot" 선택
3. "제거" 클릭

또는

1. 시작 메뉴 → "IT HelpDesk Bot" → "제거"

---

## 설치 프로그램 커스터마이징

### `setup_script.iss` 파일 수정:

#### 앱 정보 변경:
```iss
#define AppName "IT HelpDesk Bot"
#define AppVersion "1.0.0"
#define AppPublisher "회사명"
```

#### 아이콘 추가:
```iss
SetupIconFile=icon.ico
```

#### 라이선스 파일 추가:
```iss
LicenseFile=LICENSE.txt
```

#### 추가 파일 포함:
```iss
[Files]
Source: "추가파일.txt"; DestDir: "{app}"; Flags: ignoreversion
```

---

## 배포 방법

### 1. 단일 파일 배포
- `installer\ITHelpDeskBot_Setup.exe` 파일만 배포
- 사용자가 실행하면 자동 설치

### 2. 네트워크 배포
- 공유 폴더에 설치 파일 업로드
- 사용자들이 다운로드하여 설치

### 3. USB 배포
- USB에 설치 파일 복사
- 각 컴퓨터에서 설치

---

## 문제 해결

### 문제 1: "Inno Setup을 찾을 수 없습니다"

**해결:**
- Inno Setup이 설치되어 있는지 확인
- `build_installer.bat`에서 경로 확인
- 수동으로 Inno Setup Compiler 실행

### 문제 2: 빌드 실패

**해결:**
- `dist\ITHelpDeskBot.exe` 파일이 존재하는지 확인
- `build_exe.bat`를 먼저 실행
- Inno Setup 로그 확인

### 문제 3: 설치 프로그램이 실행되지 않음

**해결:**
- Windows Defender 또는 백신 프로그램 확인
- 관리자 권한으로 실행
- 호환성 모드 설정

---

## 고급 설정

### 자동 업데이트 기능 추가:
- 버전 체크 API 연동
- 업데이트 알림 기능

### 데이터베이스 자동 설정:
- MariaDB 자동 설치 (선택사항)
- 환경 변수 자동 설정

### 서비스로 설치:
- Windows 서비스로 등록
- 부팅 시 자동 시작

---

## 요약

1. **Inno Setup 설치** (무료)
2. **`build_installer.bat` 실행**
3. **`installer\ITHelpDeskBot_Setup.exe` 배포**
4. **사용자들이 설치 프로그램 실행**

**완료!** 🎉
