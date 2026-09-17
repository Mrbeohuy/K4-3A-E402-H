# CP3 Prototype

## Architecture

The frontend is still a small HTML/CSS/JS prototype, but the central decision is handled by a backend:

1. Student enters a question in `index.html`.
2. `app.js` sends the question to `POST /api/ask`.
3. `server.py` calls the CP3 pipeline in `cp3_core.py`.
4. `local_data.py` retrieves the top relevant snippets from local `data/vlearn-pack/`.
5. `cp3_core.py` sends only those retrieved snippets plus the question to Gemini.
6. Gemini returns structured JSON with `ANSWER`, `CLARIFY`, or `OUT_OF_SCOPE`.
7. Backend validates the JSON and source IDs, writes a secret-free trace, then returns the result to the UI.

## Local Data Use

- Knowledge source: `data/vlearn-pack/transcript/` and `data/vlearn-pack/slides/`.
- Golden-set patterns: `data/discord-pack/k4_messages.csv`.
- Stable source IDs are created locally, for example `VLEARN_T04_SEG_049` and `VLEARN_DAY1_SLIDE_015`.
- Retrieval is simple keyword scoring over local chunks and returns at most 5 snippets per question.
- Gemini does not receive the whole data pack. It receives only the retrieved snippets for that request.
- `data/` is local-only and ignored by Git. Do not commit or push it.

## Real AI vs Mock

- Real AI: central decision `ANSWER` / `CLARIFY` / `OUT_OF_SCOPE` when `GEMINI_API_KEY` is configured.
- Real local data: VLearn transcript/slide snippets are used as answer context.
- Evaluation data: at least 10 golden cases are derived from Discord chatlog message IDs and short excerpts.
- Legacy demo data: `knowledge_sources.json` is kept only for old unit tests/reference and is no longer the default CP3 knowledge source.

## Setup

From project root:

```powershell
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Open `.env` and replace `YOUR_KEY_HERE` with your real Gemini API key:

```text
GEMINI_API_KEY=YOUR_REAL_KEY_HERE
GEMINI_MODEL=gemini-3.6-flash
```

Do not commit `.env`. The repo should only contain `.env.example`.

## Run Backend and UI

```powershell
python codebase/server.py
```

Open:

```text
http://127.0.0.1:5000
```

Do not call Gemini directly from the browser. The browser calls the local backend so the API key stays in the environment.

## Run Evaluation

```powershell
python eval/run_eval.py
```

The runner reads `eval/golden_set.json`, calls the same retrieval + Gemini pipeline as the UI, writes trace to `eval/traces/cp3-run1.jsonl`, and writes results only after a real AI run:

- `eval/run1-results.json`
- `eval/run1-summary.md`

If `GEMINI_API_KEY` is missing, the runner stops and does not create fake Run 1 results.

## Trace

Manual UI/API calls write to:

```text
eval/traces/cp3-manual.jsonl
```

Eval Run 1 writes to:

```text
eval/traces/cp3-run1.jsonl
```

Traces include timestamp, model, user input, retrieved source IDs, model decision, model answer, returned source IDs, latency, and success/error. They must not include `GEMINI_API_KEY`, Authorization headers, or secret tokens.
