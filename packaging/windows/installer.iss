; ===================================================================
; Stickity Stacks - Inno Setup Installer Script
; ===================================================================

#define MyAppName "Stickity Stacks"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "T-Chartrand"
#define MyAppURL "https://github.com/T-Chartrand/Stickity_Stacks"
#define MyAppExeName "StickityStacks.exe"

[Setup]
AppId={{C3A7D812-4F9E-4B2A-A651-8D0E5F3C1B7A}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=LICENSE
OutputDir=installer_output
OutputBaseFilename=StickityStacks_Setup_v{#MyAppVersion}
SetupIconFile=stickity_stacks.ico
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
PrivilegesRequired=lowest
DisableProgramGroupPage=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "stickity_stacks.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "README_WINDOWS.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "LICENSE"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\stickity_stacks.ico"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\stickity_stacks.ico"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: files; Name: "{userappdata}\stickity_stacks_notes_win.json"
