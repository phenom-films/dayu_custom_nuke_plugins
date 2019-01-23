
@echo off
set MY_CUSTOM_FITMENT=%~dp0/nuke
set NUKE_PATH=%NUKE_PATH%;%~dp0/fitment/nuke_fitment
C:
cd %ProgramFiles%
for /d %%i in (nuke*) do ( set dirname=%%i )
cd %dirname%
for  %%i in (nuke*.exe) do ( set exename=%%i )
%exename% --nukex

