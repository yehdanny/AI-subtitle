@echo off
chcp 65001 > nul
echo ============================================
echo   AI 字幕生成器 - EXE 打包腳本
echo ============================================
echo.

call .venv\Scripts\activate

echo [1/2] 清除舊版本 build / dist...
if exist build rmdir /s /q build
if exist dist  rmdir /s /q dist

echo [2/2] 開始打包（需要數分鐘，請耐心等候）...
pyinstaller "AI字幕.spec" --clean

echo.
if exist "dist\AI字幕\AI字幕.exe" (
    echo ============================================
    echo   打包成功！
    echo   輸出位置：dist\AI字幕\
    echo   執行檔  ：dist\AI字幕\AI字幕.exe
    echo ============================================
) else (
    echo [ERROR] 打包失敗，請檢查上方錯誤訊息。
)

pause
