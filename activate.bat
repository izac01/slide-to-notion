@echo off
cd /d %~dp0
call metagpt_env\Scripts\activate.bat
echo.
echo ================================
echo 🚀 Starting your AI Dev Team...
echo ================================
echo.

metagpt "Write a PRD for a Windows app that helps me organize daily tasks, assign work to team members, and review the code before release."

pause
