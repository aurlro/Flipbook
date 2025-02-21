@echo off
echo Installation des outils necessaires...

REM Installation de Visual Studio Build Tools
echo Installation de Visual Studio Build Tools...
curl -L "https://aka.ms/vs/17/release/vs_buildtools.exe" -o vs_buildtools.exe
start /wait vs_buildtools.exe --quiet --wait --norestart --nocache ^
    --installPath "%ProgramFiles(x86)%\Microsoft Visual Studio\2022\BuildTools" ^
    --add Microsoft.VisualStudio.Workload.NativeDesktop ^
    --add Microsoft.VisualStudio.Component.VC.Tools.x86.x64 ^
    --add Microsoft.VisualStudio.Component.Windows10SDK.19041

del vs_buildtools.exe

REM Vérification de l'installation
if not exist "%ProgramFiles(x86)%\Microsoft Visual Studio\2022\BuildTools\VC\Tools\MSVC" (
    echo Erreur: Visual Studio Build Tools n'a pas ete installe correctement.
    exit /b 1
)

echo Installation terminee avec succes!
pause