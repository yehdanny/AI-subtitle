"""
EXE 入口：自動開啟瀏覽器，並以非 debug 模式啟動 Flask。
"""
import sys
import os
import threading
import webbrowser
import time

# 當 PyInstaller 打包後，切換工作目錄到 EXE 所在位置
if getattr(sys, "frozen", False):
    os.chdir(os.path.dirname(sys.executable))

PORT = 5000


def _open_browser():
    time.sleep(1.8)
    webbrowser.open(f"http://127.0.0.1:{PORT}")


if __name__ == "__main__":
    print("=" * 52)
    print("  AI 字幕生成器")
    print(f"  http://127.0.0.1:{PORT}  （關閉此視窗即停止服務）")
    print("=" * 52)

    threading.Thread(target=_open_browser, daemon=True).start()

    from app import app
    app.run(host="127.0.0.1", port=PORT, debug=False, use_reloader=False)
