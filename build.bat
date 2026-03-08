@echo off
echo ============================================
echo   AI Subtitle Generator - Build EXE
echo ============================================
echo.

call .venv\Scripts\activate

echo [1/2] Removing old build / dist...
if exist build rmdir /s /q build
if exist dist  rmdir /s /q dist

echo [2/2] Building EXE (may take a few minutes)...
pyinstaller build.spec --clean

echo.
if exist "dist\AI-Subtitle\AI-Subtitle.exe" (
    echo ============================================
    echo   Build SUCCESS!
    echo   Output : dist\AI-Subtitle\
    echo   EXE    : dist\AI-Subtitle\AI-Subtitle.exe
    echo ============================================
) else (
    echo [ERROR] Build FAILED. Check the error messages above.
)

pause
