# HW2 — Audio Pipeline

A Python script that takes a text input, generates speech in two different voices using OpenAI TTS, transcribes the audio back using OpenAI Whisper, and compares the result. Tracks cost and latency for every API call.

---

## Features

- **Text-to-Speech** — generates MP3 audio in two voices (`nova` and `alloy`)
- **Speech-to-Text** — transcribes audio using Whisper (`whisper-1`)
- **Round-trip comparison** — compares original text vs transcript with word overlap accuracy
- **Cost & latency tracking** — logs timestamp, model, input size, duration, and cost per call
- **Error handling** — retries on API failure, handles missing files and unsupported formats

---

## Expected Output

```
=== HW2 Audio Pipeline ===

[1/4] Generating speech with voice: nova
  Text: "Machine learning models learn patterns from data and improve..."
  Generated in 3.70s
  File: audio-output/voice_nova_sample.mp3 (85.78 KB)
  Cost: $0.0011

[2/4] Generating speech with voice: alloy
  Text: "Machine learning models learn patterns from data and improve..."
  Generated in 2.13s
  File: audio-output/voice_alloy_sample.mp3 (88.12 KB)
  Cost: $0.0011

[3/4] Transcribing audio-output/voice_nova_sample.mp3
  Transcript: "Machine learning models learn patterns from data and improve over time."
  Transcribed in 1.54s
  Audio duration: ~5.5s
  Cost: $0.0005

[4/4] Comparing original vs transcribed text
  Original:    "Machine learning models learn patterns from data and improve over time."
  Transcribed: "Machine learning models learn patterns from data and improve over time."
  Word overlap accuracy: 100.0%

=== Cost and Latency Summary ===
  TTS calls:  2 | Total cost: $0.0021 | Avg latency: 2.92s
  STT calls:  1 | Total cost: $0.0005 | Avg latency: 1.54s
  Pipeline total: $0.0027

=== Pipeline complete ===
```

---

## Project Structure

```
hw2/
├── hw2-audio-pipeline.py      # Main pipeline script
├── reflection.md              # Data governance reflection
├── requirements.txt           # Python dependencies
├── .env.example               # API key template (no real keys)
├── README.md                  # This file
└── audio-output/
    ├── voice_nova_sample.mp3  # TTS output - nova voice
    └── voice_alloy_sample.mp3 # TTS output - alloy voice
```

---

## Data Governance Summary
Key points:

- **Consent** — users must explicitly agree before any real audio is recorded or sent to an API
- **Retention** — synthetic audio can be deleted after 7 days; real/medical audio should be deleted immediately after transcription
- **PII risks** — audio carries voice biometrics, accent, background sounds, and metadata that plain text does not
- **Capstone** — our team deferred audio for now; if added later, consent flow and auto-deletion will be required