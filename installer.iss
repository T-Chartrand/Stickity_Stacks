#define MyAppName "Stickity Stacks"

#ifndef MyAppVersion
#define MyAppVersion "1.0.1"
#endif

#define MyAppPublisher "Tyrrell Chartrand"
#define MyAppURL "https://github.com/T-Chartrand/Stickity_Stacks"
#define MyAppExeName "StickityStacks.exe"

[Setup]
AppId=TChartrand.StickityStacks
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}

DefaultDirName={localappdata}\Programs\Stickity Stacks
DefaultGroupName=Stickity Stacks
PrivilegesRequired=lowest

OutputDir=installer_output
OutputBaseFilename=StickityStacks_Setup_v{#MyAppVersion}
SetupIconFile=stickity_stacks.ico
UninstallDisplayIcon={app}\{#MyAppExeName}

Compression=lzma2
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional shortcuts:"

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent
