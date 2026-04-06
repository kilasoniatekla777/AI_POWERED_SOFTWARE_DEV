# HW2 Data Governance Reflection


**Assignment:** Homework 2 — Audio Pipeline

---

## 1. Consent for Real User Audio

In my pipeline, the audio is synthetic (`voice_nova_sample.mp3` and `voice_alloy_sample.mp3`), so no real person is recorded. But if users could record their own voice, we would need a clear consent screen before recording.

The screen would say: "This app will record your voice, send it to OpenAI Whisper for transcription, and delete the audio within 24 hours. Do you agree?" Users would tap "I agree" to continue. Users should also be able to revoke consent later in settings, and the system should delete all their audio and transcripts within 30 days and confirm by email.

If the audio is used for anything else, like improving models, users must opt in separately.

---

## 2. Audio Retention

Retention depends on the app:

- **Study app:** My synthetic audio files are small (~85 KB each) and can be deleted after 7 days because the text can always be used to regenerate them.
- **Customer service:** Calls should be kept 90 days for quality checks, then raw audio deleted but transcripts kept longer for legal reasons.
- **Medical intake:** Audio is very sensitive. It should be deleted within hours after transcription is confirmed. Transcripts stay 7–10 years and only authorized staff can access them.

The main idea: keep only what you need, for as short as possible.

---

## 3. PII in Audio

Audio has more privacy risks than text:

- **Voice biometrics:** Voices are unique and can identify a person or be cloned with AI.
- **Accent and language:** Can reveal a person's origin or ethnicity.
- **Background sounds:** Can reveal location or home environment.
- **Emotional state:** Tone of voice shows stress, anger, or anxiety.
- **File metadata:** Can include device type, timestamp, and sometimes GPS.

Text transcripts don't carry these risks, which is why audio should be deleted after use rather than kept alongside the transcript.

---

## 4. Application to My Capstone

Our team decided not to use audio yet in our capstone. If we add it later, we would need:

- A consent screen before any recording starts
- Auto-deletion of raw audio within 24 hours
- Clear notice that voice data is sent to OpenAI Whisper
- A way for EU users to request full deletion of their data

Running this pipeline made me realize that even synthetic audio files sitting in the `audio-output/` folder need a plan for storage and deletion. Real user audio would need much stricter rules to keep people's data safe.
