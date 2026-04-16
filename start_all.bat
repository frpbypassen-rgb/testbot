@echo off
title Al-Ahram System Launcher
echo 🚀 Starting Al-Ahram Mobile Services System...

:: تشغيل بوت العميل في نافذة مستقلة
start "Customer Bot" cmd /k ".venv\Scripts\python.exe Customer_Bot/main.py"

:: انتظار 3 ثواني
timeout /t 3

:: تشغيل بوت الإدارة في نافذة مستقلة
start "Admin Bot" cmd /k ".venv\Scripts\python.exe Admin_bot/admin_main.py"

echo ✅ Both bots are running in separate windows.
pause