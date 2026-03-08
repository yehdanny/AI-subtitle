# AI 字幕生成器

本地端 AI 字幕生成工具，上傳影片後即可自動產生逐字稿字幕，支援多語言辨識、時間軸對齊、影片預覽與 SRT 匯出。

---

## 畫面預覽

### 1. 首頁上傳介面
拖曳或點擊上傳影片，支援 MP4、MKV、MOV、AVI、WebM 等格式。

![上傳介面](docs/screenshots/01_upload.png)

---

### 2. 影片預覽 + 字幕清單
左側影片播放器搭配可拖拉時間軸；右側依時間順序列出每段字幕的開始／結束時間與文字。

![主介面](docs/screenshots/02_main.png)

---

### 3. 字幕即時同步
影片播放時，當前字幕自動高亮（橘色左邊框）並滾動至可視範圍，同時疊加顯示於影片畫面下方。

![字幕同步](docs/screenshots/03_subtitle_sync.png)

---

### 4. 模型與語言選擇
右上角可選擇 Whisper 模型大小（Tiny → Large）與辨識語言（自動偵測或手動指定）。

![設定選項](docs/screenshots/04_settings.png)

---

### 5. 匯出 SRT
字幕產生後，點擊「匯出 SRT」即可下載標準格式字幕檔，可直接匯入 Premiere、DaVinci Resolve 等剪輯軟體。

![匯出SRT](docs/screenshots/05_export.png)

---

## 功能特色

| 功能 | 說明 |
|------|------|
| 本地端處理 | 影片與字幕資料不離開你的電腦 |
| AI 語音辨識 | 使用 OpenAI Whisper，準確率高 |
| 多語言支援 | 中文、英文、日文、韓文等 99 種語言 |
| 時間軸字幕 | 精確到毫秒的開始／結束時間 |
| 影片預覽 | 播放器搭配可拖拉時間軸 |
| 字幕同步 | 播放時自動高亮對應字幕 |
| 點擊跳轉 | 點擊任一字幕即跳至該時間點 |
| 匯出 SRT | 標準字幕格式，相容各大剪輯軟體 |
| GPU 加速 | 自動偵測 NVIDIA GPU，速度大幅提升 |

---

## 快速開始

### 方式一：直接執行 EXE（推薦）

1. 執行 `build.bat` 打包（僅需一次）
2. 進入 `dist\AI字幕\` 資料夾
3. 雙擊 `AI字幕.exe`
4. 瀏覽器自動開啟 `http://127.0.0.1:5000`

### 方式二：Python 環境執行

```bash
# 建立虛擬環境並安裝套件
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# 啟動
python app.py
```

開啟瀏覽器前往 `http://127.0.0.1:5000`

---

## 系統需求

| 項目 | 最低需求 |
|------|---------|
| OS | Windows 10/11 |
| Python | 3.10 以上 |
| RAM | 8 GB（建議 16 GB） |
| GPU | NVIDIA（選用，大幅加速） |
| CUDA | 12.4（使用 GPU 時需要） |

> **不需要手動安裝 ffmpeg**，已透過 `imageio-ffmpeg` 內建。

---

## Whisper 模型比較

| 模型 | 大小 | 速度 | 準確率 | 建議場景 |
|------|------|------|--------|---------|
| Tiny | 75 MB | ★★★★★ | ★★☆☆☆ | 快速測試 |
| Base | 145 MB | ★★★★☆ | ★★★☆☆ | 日常使用（預設） |
| Small | 466 MB | ★★★☆☆ | ★★★★☆ | 較高準確率 |
| Medium | 1.5 GB | ★★☆☆☆ | ★★★★★ | 高品質輸出 |
| Large | 3 GB | ★☆☆☆☆ | ★★★★★ | 最高準確率 |

> 模型於首次使用時自動下載至 `%USERPROFILE%\.cache\whisper\`

---

## 鍵盤快捷鍵

| 按鍵 | 功能 |
|------|------|
| `Space` | 播放 / 暫停 |
| `←` | 後退 5 秒 |
| `→` | 前進 5 秒 |

---

## 技術堆疊

- **後端**：Python · Flask
- **語音辨識**：OpenAI Whisper
- **深度學習**：PyTorch 2.6 (CUDA 12.4)
- **音訊解碼**：imageio-ffmpeg
- **前端**：原生 HTML / CSS / JavaScript
