# Shorts & Video Downloader (短影音下載器)

這是一個功能強大且易於使用的網頁應用程式，專為批量下載 TikTok 和 YouTube 影片而設計。使用 Python、FastAPI 和現代網頁技術構建。

## 功能特色

### TikTok 下載器
- **批量下載**：一次下載多個 TikTok 影片。
- **進度追蹤**：提供獲取影片列表和下載過程的視覺化進度條。
- **暫停/繼續**：支援暫停和繼續批量下載的功能。
- **畫質控制**：預設下載高畫質影片 (720p+)。

### YouTube 下載器
- **批量支援**：高效處理多個 YouTube 影片下載。
- **互動流程**：輕鬆獲取列表、選擇影片並下載。
- **優化介面**：乾淨直觀的下載管理介面。

## 技術棧

- **後端**：Python 3.12+, FastAPI, Uvicorn
- **前端**：HTML5, CSS3, JavaScript (Vanilla)
- **工具**：`yt-dlp` (核心下載引擎)

## 安裝指南

1.  **複製專案 (Clone)**
    ```bash
    git clone https://github.com/KANG011111/tk-dl-1123.git
    cd shorts-download1121
    ```

2.  **建立虛擬環境**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Windows 使用: .venv\Scripts\activate
    ```

3.  **安裝依賴套件**
    ```bash
    pip install -r requirements.txt
    ```

4.  **設定環境變數**
    複製範例環境檔案並進行配置（如有需要）：
    ```bash
    cp .env.example .env
    ```

## 使用說明

1.  **啟動伺服器**
    ```bash
    uvicorn src.shorts_dl.main:app --reload
    ```

2.  **開啟應用程式**
    打開瀏覽器並前往 `http://localhost:8000`。

3.  **開始下載**
    - 前往 TikTok 或 YouTube 區塊。
    - 貼上個人主頁連結或影片連結。
    - 點擊 "Fetch" (獲取) 來取得影片列表。
    - 選擇想要下載的影片並點擊 "Download" (下載)。

## 專案結構

```
shorts-download1121/
├── src/
│   └── shorts_dl/
│       ├── main.py          # 應用程式入口
│       ├── schemas.py       # 資料模型
│       └── ...
├── downloads/               # 預設下載目錄
├── public/                  # 靜態資源 (CSS, JS)
├── requirements.txt         # 專案依賴列表
└── README.md                # 專案說明文件
```

## 授權

[MIT License](LICENSE)
