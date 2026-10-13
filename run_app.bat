@echo off
chcp 65001 >nul
title Creative Ads CHECK - Hoàng Duy Ads (Local Server)
color 0B

echo ==============================================================================
echo       CREATIVE ADS CHECK - HOÀNG DUY ADS (LOCAL AI GATEWAY)
echo ==============================================================================
echo.
echo [1/3] Kiểm tra môi trường Python...
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [LỖI] Không tìm thấy Python trong hệ thống! Vui lòng cài đặt Python 3.10+ và thêm vào PATH.
    pause
    exit /b 1
)

echo [2/3] Kiểm tra thư viện phụ thuộc (FastAPI, Google GenAI, Uvicorn)...
python -m pip install -r requirements.txt --quiet --no-warn-script-location

echo [3/3] Khởi chạy Backend Gateway trên Loopback (127.0.0.1:8000)...
echo.
echo ==============================================================================
echo   Server đang chạy tại: http://127.0.0.1:8000
echo   API Health Check:     http://127.0.0.1:8000/api/health
echo   Đang tự động mở trình duyệt...
echo   (Nhấn Ctrl+C để dừng server khi không sử dụng)
echo ==============================================================================
echo.

start "" "http://127.0.0.1:8000"

python -m uvicorn main:app --host 127.0.0.1 --port 8000
pause
