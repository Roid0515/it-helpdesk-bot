; Inno Setup 설치 스크립트
; IT HelpDesk Bot 설치 프로그램 생성용

#define AppName "IT HelpDesk Bot"
#define AppVersion "1.0.0"
#define AppPublisher "IT HelpDesk"
#define AppURL "https://github.com/Roid0515/it-helpdesk-bot"
#define AppExeName "ITHelpDeskBot.exe"

[Setup]
; 설치 프로그램 기본 정보
AppId={{A1B2C3D4-E5F6-4A5B-8C9D-0E1F2A3B4C5D}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
AppPublisherURL={#AppURL}
AppSupportURL={#AppURL}
AppUpdatesURL={#AppURL}
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
AllowNoIcons=yes
LicenseFile=
InfoBeforeFile=
InfoAfterFile=
OutputDir=installer
OutputBaseFilename=ITHelpDeskBot_Setup
SetupIconFile=
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "korean"; MessagesFile: "compiler:Languages\Korean.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1

[Files]
; 실행 파일
Source: "dist\ITHelpDeskBot.exe"; DestDir: "{app}"; Flags: ignoreversion
; 데이터베이스 파일 (초기 생성용)
Source: "helpdesk.db"; DestDir: "{app}"; Flags: ignoreversion onlyifdoesntexist
; README 및 문서
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion isreadme
Source: "MARIADB_SETUP.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "DATABASE_GUIDE.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\{#AppExeName}"
Name: "{group}\{cm:UninstallProgram,{#AppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\{#AppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(AppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
procedure InitializeWizard;
begin
  // 설치 전 초기화 작업
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // 설치 후 작업 (필요시)
  end;
end;
