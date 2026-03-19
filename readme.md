# HW1

## What I Built
A Python script that calls two Gemini models with the same prompt and compares their responses, token counts, latency, and cost.

## How to Run
1. `python3 -m venv venv && source venv/bin/activate`
2. `pip install google-genai python-dotenv`
3. Copy `.env.example` to `.env` and add your Gemini API key
4. `python hw01_script.py`

## Cost Analysis

| Call | Model | Input Tokens | Output Tokens | Total Tokens | Latency (ms) | Cost (paid equiv.) |
|------|-------|-------------|--------------|-------------|-------------|-------------------|
| 1 | gemini-3-flash-preview | 32 | 142 | 367 | 3411 | $0.00006000 |
| 2 | gemini-3.1-flash-lite-preview | 32 | 113 | 145 | 1707 | $0.00003630 |

## Reflection
I first tried gemini-2.0-flash on my own before using the professor's suggested models, and immediately got a quota exhausted error which I did not expect at all. I honestly did not think token counts would be that high either — I assumed a short prompt would use very few tokens on both sides. Switching to the correct models fixed the problem instantly, and it surprised me that such a small change also made the calls significantly cheaper. I expected both models to perform similarly in terms of speed, but gemini-3.1-flash-lite-preview was almost twice as fast at 1707ms versus 3411ms. The biggest takeaway for me was that model choice has a real impact on cost and speed, even for a tiny two-sentence prompt.
