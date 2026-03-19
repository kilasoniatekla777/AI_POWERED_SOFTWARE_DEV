"""
CS-AI-2025 | Lab 1 | Homework 1
Spring 2026 | Kutaisi International University
"""

import os
import time
from dotenv import load_dotenv

load_dotenv()

try:
    import google.genai as genai
except ImportError:
    print("ERROR: google-genai package not installed. Run: pip install google-genai")
    exit(1)

MODELS = [
    "gemini-3-flash-preview",
    "gemini-3.1-flash-lite-preview",
]

PROMPT = (
    "A farmer has 17 sheep. All but 9 run away. "
    "How many sheep does the farmer have left? Explain your reasoning step by step."
)

COSTS = {
    "gemini-3-flash-preview":       {"input": 0.10, "output": 0.40},
    "gemini-3.1-flash-lite-preview": {"input": 0.075, "output": 0.30},
}

def main():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not found. Check your .env file.")
        exit(1)

    client = genai.Client(api_key=api_key)

    print(f"\nCS-AI-2025 HW1 — Two Model Comparison")
    print(f"Prompt: {PROMPT}\n")

    results = []

    for model_name in MODELS:
        print(f"\n{'='*60}")
        print(f"Model: {model_name}")
        print('='*60)

        start_time = time.perf_counter()
        response = client.models.generate_content(
            model=model_name,
            contents=PROMPT
        )
        latency_ms = (time.perf_counter() - start_time) * 1000

        usage = response.usage_metadata
        input_tokens  = usage.prompt_token_count
        output_tokens = usage.candidates_token_count
        total_tokens  = usage.total_token_count

        cost_per_m = COSTS.get(model_name, {"input": 0, "output": 0})
        cost = (input_tokens  / 1_000_000 * cost_per_m["input"] +
                output_tokens / 1_000_000 * cost_per_m["output"])

        print(f"\nRESPONSE:")
        print("─" * 40)
        print(response.text)
        print("─" * 40)
        print(f"\nTOKEN USAGE:")
        print(f"  Input tokens:  {input_tokens}")
        print(f"  Output tokens: {output_tokens}")
        print(f"  Total tokens:  {total_tokens}")
        print(f"  Latency:       {latency_ms:.0f} ms")
        print(f"  Cost (paid tier equivalent): ${cost:.8f}")

        results.append({
            "model": model_name,
            "input": input_tokens,
            "output": output_tokens,
            "total": total_tokens,
            "latency_ms": round(latency_ms),
            "cost": cost,
        })

    print(f"\n\n{'='*60}")
    print("COST SUMMARY TABLE")
    print(f"{'='*60}")
    print(f"{'Call':<5} {'Model':<30} {'Input':>7} {'Output':>8} {'Total':>7} {'Latency':>12} {'Cost':>18}")
    print("-" * 95)
    for i, r in enumerate(results, 1):
        print(f"{i:<5} {r['model']:<30} {r['input']:>7} {r['output']:>8} {r['total']:>7} {r['latency_ms']:>10}ms  ${r['cost']:.8f}")

    print("\n✓ HW1 complete.")

if __name__ == "__main__":
    main()
