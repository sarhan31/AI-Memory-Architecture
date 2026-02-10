@echo off
echo ============================================================
echo 🏠 Starting AI Memory System in LOCAL MODE
echo ============================================================
echo.
echo ✅ No API keys required
echo ✅ Fully local operation
echo ✅ Memory features fully functional
echo.
echo ============================================================
echo.

cd /d "%~dp0"
call venv\Scripts\activate.bat
python run_orchestrator.py

pause
