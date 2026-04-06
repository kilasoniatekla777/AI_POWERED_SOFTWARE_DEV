import os
import time
import datetime
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

OUTPUT_DIR = "audio-output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

TEXT = "Machine learning models learn patterns from data and improve over time."


call_log = []
tts_cost_total = 0.0
stt_cost_total = 0.0


def log_call(call_type, model, latency, input_size, cost):
    call_log.append({
        "timestamp": datetime.datetime.now().isoformat(),
        "type": call_type,
        "model": model,
        "latency_s": round(latency, 3),
        "input_size": input_size,
        "cost_usd": round(cost, 6),
    })



def api_call_with_retry(fn, retries=1, delay=2):
    for attempt in range(retries + 1):
        try:
            return fn()
        except Exception as e:
            if attempt < retries:
                print(f"  [Retry {attempt + 1}/{retries}] Error: {e}. Retrying in {delay}s...")
                time.sleep(delay)
            else:
                raise



def tts_generate(text, voice, step_num, total_steps):
    global tts_cost_total

    print(f"\n[{step_num}/{total_steps}] Generating speech with voice: {voice}")
    print(f'  Text: "{text[:60]}..."' if len(text) > 60 else f'  Text: "{text}"')

    start = time.time()

    def call():
        return client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text,
            response_format="mp3"
        )

    response = api_call_with_retry(call)
    latency = time.time() - start

    filename = f"{OUTPUT_DIR}/voice_{voice}_sample.mp3"
    with open(filename, "wb") as f:
        f.write(response.content)

    size_kb = os.path.getsize(filename) / 1024
    cost = (len(text) / 1000) * 0.015
    tts_cost_total += cost

    log_call("TTS", "tts-1", latency, f"{len(text)} chars", cost)

    print(f"  Generated in {latency:.2f}s")
    print(f"  File: {filename} ({size_kb:.2f} KB)")
    print(f"  Cost: ${cost:.4f}")

    return filename



def get_audio_duration_seconds(file_path):
    """Estimate MP3 duration from file size (assumes ~128kbps)."""
    try:
        size_bytes = os.path.getsize(file_path)
        return size_bytes / 16000  
    except Exception:
        return 8.0



def stt_transcribe(file_path, step_num, total_steps):
    global stt_cost_total

    print(f"\n[{step_num}/{total_steps}] Transcribing {file_path}")

    if not os.path.exists(file_path):
        print(f"  Error: File not found -- {file_path}")
        return None

    supported_formats = (".mp3", ".wav", ".mp4", ".m4a", ".webm", ".mpeg", ".mpga")
    if not file_path.lower().endswith(supported_formats):
        print(f"  Error: Unsupported audio format -- {file_path}")
        print(f"  Supported formats: {', '.join(supported_formats)}")
        return None

    start = time.time()

    def call():
        with open(file_path, "rb") as f:
            return client.audio.transcriptions.create(
                model="whisper-1",
                file=f
            )

    transcript = api_call_with_retry(call)
    latency = time.time() - start

    text = transcript.text
    duration_seconds = get_audio_duration_seconds(file_path)
    audio_minutes = duration_seconds / 60
    cost = audio_minutes * 0.006
    stt_cost_total += cost

    log_call("STT", "whisper-1", latency, f"{duration_seconds:.1f}s audio", cost)

    print(f'  Transcript: "{text}"')
    print(f"  Transcribed in {latency:.2f}s")
    print(f"  Audio duration: ~{duration_seconds:.1f}s")
    print(f"  Cost: ${cost:.4f}")

    return text



def compare_text(original, transcribed, step_num, total_steps):
    print(f"\n[{step_num}/{total_steps}] Comparing original vs transcribed text")

    original_words = original.lower().split()
    transcribed_words = set(transcribed.lower().split())

    matches = sum(1 for w in original_words if w in transcribed_words)
    accuracy = (matches / len(original_words)) * 100 if original_words else 0

    print(f'  Original:    "{original}"')
    print(f'  Transcribed: "{transcribed}"')
    print(f"  Word overlap accuracy: {accuracy:.1f}%")

    return accuracy



def summary():
    print("\n=== Cost and Latency Summary ===")

    tts_calls = [c for c in call_log if c["type"] == "TTS"]
    stt_calls = [c for c in call_log if c["type"] == "STT"]

    if tts_calls:
        avg_tts = sum(c["latency_s"] for c in tts_calls) / len(tts_calls)
        print(f"  TTS calls:  {len(tts_calls)} | Total cost: ${tts_cost_total:.4f} | Avg latency: {avg_tts:.2f}s")

    if stt_calls:
        avg_stt = sum(c["latency_s"] for c in stt_calls) / len(stt_calls)
        print(f"  STT calls:  {len(stt_calls)} | Total cost: ${stt_cost_total:.4f} | Avg latency: {avg_stt:.2f}s")

    print(f"  Pipeline total: ${(tts_cost_total + stt_cost_total):.4f}")

    print("\n  Detailed call log:")
    for entry in call_log:
        print(f"    [{entry['timestamp']}] {entry['type']} | model={entry['model']} | "
              f"latency={entry['latency_s']}s | input={entry['input_size']} | cost=${entry['cost_usd']:.6f}")



def main():
    print("=== HW2 Audio Pipeline ===")

    total_steps = 4

    try:
        file_nova  = tts_generate(TEXT, "nova",  step_num=1, total_steps=total_steps)
        file_alloy = tts_generate(TEXT, "alloy", step_num=2, total_steps=total_steps)

        transcript = stt_transcribe(file_nova, step_num=3, total_steps=total_steps)

        if transcript:
            compare_text(TEXT, transcript, step_num=4, total_steps=total_steps)
        else:
            print("\n[4/4] Skipping comparison -- transcription failed.")

        summary()
        print("\n=== Pipeline complete ===")

    except Exception as e:
        print(f"\n[Error] Pipeline failed: {e}")
        print("Check your OPENAI_API_KEY and internet connection.")


if __name__ == "__main__":
    main()