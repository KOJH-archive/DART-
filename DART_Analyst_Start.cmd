@echo off
setlocal
title DART Analyst

powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0run_windows.ps1" %*
set "launcher_exit=%ERRORLEVEL%"

if /I "%~1"=="-CheckOnly" exit /b %launcher_exit%

if not "%launcher_exit%"=="0" (
  echo.
  echo Launch failed. Review the message above.
)

echo.
echo Press any key to close this window.
pause >nul
exit /b %launcher_exit%
