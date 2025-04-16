from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from typing import List, Optional
import re
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="YouTube Transcript Extractor", 
              description="An API to extract transcripts from YouTube videos")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TranscriptRequest(BaseModel):
    youtube_url: HttpUrl
    language_code: Optional[str] = "en"

class TranscriptSegment(BaseModel):
    text: str
    start: float
    duration: float

class TranscriptResponse(BaseModel):
    video_id: str
    transcript: List[TranscriptSegment]
    full_text: str

def extract_video_id(youtube_url: str) -> str:
    """Extract the video ID from a YouTube URL."""
    # Pattern to match YouTube video IDs
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',  # Standard YouTube URLs
        r'(?:embed\/)([0-9A-Za-z_-]{11})',  # Embedded URLs
        r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})'  # Shortened URLs
    ]
    
    for pattern in patterns:
        match = re.search(pattern, youtube_url)
        if match:
            return match.group(1)
    
    raise HTTPException(status_code=400, detail="Could not extract video ID from URL")

@app.post("/extract-transcript/", response_model=TranscriptResponse)
async def extract_transcript(request: TranscriptRequest):
    try:
        # Extract video ID from the URL
        video_id = extract_video_id(str(request.youtube_url))
        
        # Get the transcript directly without using the list_transcripts method
        # This is a simpler approach that avoids the FetchedTranscriptSnippet issue
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id, languages=[request.language_code])
        
        # Convert to our response model format
        segments = [
            TranscriptSegment(
                text=item["text"],
                start=item["start"],
                duration=item["duration"]
            ) for item in transcript_data
        ]
        
        # Combine all text into a single string with proper spacing
        full_text = " ".join([item["text"] for item in transcript_data])
        
        return TranscriptResponse(
            video_id=video_id,
            transcript=segments,
            full_text=full_text
        )
    
    except TranscriptsDisabled:
        raise HTTPException(status_code=404, detail="Transcripts are disabled for this video")
    except NoTranscriptFound:
        raise HTTPException(status_code=404, detail=f"No transcript found for this video in language '{request.language_code}'")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Add a route to serve the frontend
@app.get("/", response_class=FileResponse)
async def serve_frontend():
    return FileResponse("static/index.html")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)