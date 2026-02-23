# Video Generator

An automated pipeline that converts a text prompt into a fully AI-generated narrative video, handling script creation, visual generation, voiceover synthesis, and final video assembly end-to-end.

## Pipeline Steps
1. **AI Script Generation**: Generates a script utilizing Gemini, Groq, or Grok.
2. **AI Voiceover**: Converts script to audio using ElevenLabs or Edge TTS.
3. **Visuals Fetching**: Retrieves stock footage from Pexels API or generates AI images.
4. **Video Assembly**: Combines audio and visuals into an `.mp4` file using MoviePy/FFmpeg.
