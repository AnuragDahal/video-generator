# Video Generator Backend

A FastAPI-based backend for an automated video generation pipeline.

## Pipeline Steps
1. **AI Script Generation**: Generates a script utilizing Gemini, Groq, or Grok.
2. **AI Voiceover**: Converts script to audio using ElevenLabs or Edge TTS.
3. **Visuals Fetching**: Retrieves stock footage from Pexels API or generates AI images.
4. **Video Assembly**: Combines audio and visuals into an `.mp4` file using MoviePy/FFmpeg.

## Project Structure
```text
backend/
├── app/
│   ├── api/            # API endpoints (versioned)
│   ├── core/           # Config and settings
│   ├── services/       # Core pipeline logic (Business Layer)
│   ├── schemas/        # Pydantic models for validation
│   ├── utils/          # Utility functions
│   └── main.py         # App initialization
├── .env                # Secret keys (Gemini, ElevenLabs, Pexels)
├── main.py             # Entry point for development
└── pyproject.toml      # Project dependencies (managed by uv)
```

## Getting Started
1. Install dependencies:
   ```bash
   uv sync
   ```
2. Set up your `.env` file with necessary API keys.
3. Run the development server:
   ```bash
   python main.py
   ```
4. Access API documentation at `http://localhost:8000/docs`
