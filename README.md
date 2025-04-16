# 🎥 YouTube Transcript Extractor API

A simple and powerful FastAPI-based REST API that allows users to extract transcripts from YouTube videos using only the video URL. This API utilizes the [`youtube-transcript-api`](https://pypi.org/project/youtube-transcript-api/) package to fetch transcripts and provides both segmented and full-text output.

---

## 📦 Features

- ✅ Extracts transcript from YouTube videos using a URL.
- ✅ Supports custom language codes (default is English).
- ✅ Returns both segmented transcripts and a full combined text.
- ✅ CORS enabled for frontend integrations.
- ✅ Static file serving for frontend integration (e.g., HTML UI).
- ✅ Robust error handling (no transcript, transcript disabled, invalid URL, etc.).

---

## 🚀 Getting Started

### 🔧 Requirements

- Python 3.8+
- pip

### 📥 Installation

1. **Clone the repository:**

```bash
git clone https://github.com/yourusername/youtube-transcript-extractor.git
cd youtube-transcript-extractor
```

2. **Create a virtual environment:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

---

## 📜 API Documentation

### ▶️ `POST /extract-transcript/`

Extract transcript from a YouTube video.

#### ✅ Request Body

```json
{
  "youtube_url": "https://www.youtube.com/watch?v=VIDEO_ID",
  "language_code": "en"  // optional, default is "en"
}
```

#### 📤 Response Example

```json
{
  "video_id": "VIDEO_ID",
  "transcript": [
    {
      "text": "Welcome to the video.",
      "start": 0.5,
      "duration": 2.3
    },
    ...
  ],
  "full_text": "Welcome to the video. This is a demo transcript..."
}
```

#### ❌ Possible Errors

- `400` - Invalid or unsupported YouTube URL
- `404` - Transcript not available or disabled
- `500` - Server error

---

## 🌐 Frontend

This API serves static files under `/static`. A basic `index.html` can be placed in the `static/` directory and will be served at the root `/`.

### 🖥️ Serving Frontend

Ensure your frontend files are placed under `static/`:

```
project/
├── static/
│   └── index.html
└── app.py
```

Access the UI by navigating to `http://localhost:8000/`.

---

## 🛡️ CORS

CORS is enabled for all origins (`*`) to allow easy integration with frontends during development. In production, **restrict this to specific origins** for security.

---

## 🧪 Running the Server

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at:  
👉 `http://localhost:8000/extract-transcript/`  
👉 `http://localhost:8000/` (for frontend)

---

## 📁 Example `.env` / `requirements.txt`

### `requirements.txt`

```
fastapi
uvicorn
pydantic
youtube-transcript-api
```

---

## 🤖 Future Improvements

- 🌍 Language auto-detection
- 🧠 Summarization of transcripts using NLP
- 🖼️ Thumbnail/title/metadata fetching from YouTube
- 💾 Caching frequent video transcripts
- 🔒 OAuth/Key-based access control

---

## 👨‍💻 Author

**E.D. Kalpa Sandakelum**  
Trainee Software Engineer | AI Enthusiast  
SYIGEN Pvt Ltd

---

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

Would you like me to generate a sample `index.html` for your static frontend too?