# Shorts & Video Downloader

A powerful and user-friendly web application for batch downloading videos from TikTok and YouTube. Built with Python, FastAPI, and modern web technologies.

## Features

### TikTok Downloader
- **Batch Downloading**: Download multiple TikTok videos at once.
- **Progress Tracking**: Visual progress indicators for fetching video lists and downloading.
- **Pause/Resume**: Control your batch downloads with pause and resume functionality.
- **Quality Control**: Default high-quality downloads (720p+).

### YouTube Downloader
- **Batch Support**: Efficiently handle multiple YouTube video downloads.
- **Interactive Flow**: Fetch lists, select videos, and download with ease.
- **Optimized UI**: Clean and intuitive interface for managing downloads.

## Tech Stack

- **Backend**: Python 3.12+, FastAPI, Uvicorn
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Utilities**: `yt-dlp` (underlying download engine)

## Installation

1.  **Clone the repository**
    ```bash
    git clone <repository-url>
    cd shorts-download1121
    ```

2.  **Create a virtual environment**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Setup Environment Variables**
    Copy the example environment file and configure it if necessary:
    ```bash
    cp .env.example .env
    ```

## Usage

1.  **Start the server**
    ```bash
    uvicorn src.shorts_dl.main:app --reload
    ```

2.  **Access the application**
    Open your browser and navigate to `http://localhost:8000`.

3.  **Start Downloading**
    - Navigate to the TikTok or YouTube section.
    - Paste the profile URL or video links.
    - Click "Fetch" to get the video list.
    - Select videos and click "Download".

## Project Structure

```
shorts-download1121/
├── src/
│   └── shorts_dl/
│       ├── main.py          # Application entry point
│       ├── schemas.py       # Data models
│       └── ...
├── downloads/               # Default download directory
├── public/                  # Static assets (CSS, JS)
├── requirements.txt         # Project dependencies
└── README.md                # Project documentation
```

## License

[MIT License](LICENSE)
