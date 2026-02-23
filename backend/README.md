# Video Generator Backend

A FastAPI-based backend for an automated video generation pipeline.

## Pipeline Steps
1. **AI Script Generation**: Generates a script utilizing Gemini, Groq, or Grok.
2. **AI Voiceover**: Converts script to audio using ElevenLabs or Edge TTS.
3. **Visuals Fetching**: Retrieves stock footage from Pexels API or generates AI images.
4. **Video Assembly**: Combines audio and visuals into an `.mp4` file using MoviePy/FFmpeg.

## Setup and Run
```bash
# Install dependencies
uv sync

# Configure Environment
# Copy API keys for Gemini, ElevenLabs, and Pexels into .env
```

## Run the Pipeline
The most reliable way to generate a video currently is using the automated test script:
```bash
# In the backend directory
set PYTHONPATH=. && python test_full_pipeline.py
```