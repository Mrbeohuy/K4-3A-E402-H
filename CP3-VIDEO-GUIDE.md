# CP3 30-Second Video Guide

Goal: show that the prototype runs end-to-end and the central decision is made by real AI through the backend.

## Before Recording

From project root, run:

```powershell
python -m pip install -r requirements.txt
Copy-Item .env.example .env
# Fill GEMINI_API_KEY in .env before starting the server.
python codebase/server.py
```

Open:

```text
http://127.0.0.1:5000
```

## 30-Second Script

1. Show the browser at `http://127.0.0.1:5000`.
2. Show the badge `CP3 — BACKEND AI DECISION`.
3. Type: `ReAct Agent là gì?`
4. Click `Gửi câu hỏi`.
5. Show loading text `Đang gọi AI...`.
6. Show the AI response with decision `ANSWER` behavior and source ID such as `DAY3_REACT_01`.
7. If time remains, type `cái này là sao?`, click submit, and show the `CLARIFY` behavior.

## What To Keep Visible

- Browser UI.
- The final answer/decision.
- Source ID for an `ANSWER` case.

Do not show your API key, terminal environment variables, `.env`, or any secret.
