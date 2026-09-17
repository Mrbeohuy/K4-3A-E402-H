# Discord Mining Summary

## Evidence Standard

Standard B: reproducible local data mining from `data/discord-pack/k4_messages.csv`.

## Headline Counts

| Metric | Count |
|---|---:|
| Total messages in pack | 1,092 |
| Non-bot messages with content | 779 |
| Bot-directed non-bot messages | 307 |
| Lookup/status pattern | 147 / 307 = 47.88% |
| Learning material / assignment pattern | 52 / 307 = 16.94% |
| Ambiguous or very short bot-directed messages | 78 / 307 = 25.41% |
| Reply or follow-up bot-directed messages | 12 / 307 = 3.91% |

## What This Supports

The data supports a real Track B pain: learners use Discord to ask the assistant for course information, status, learning materials, assignment/platform clarification, and follow-up clarification. This supports a grounded assistant that should answer only when it has evidence and otherwise clarify or refuse.

## What This Does Not Prove

- It does not prove exact time lost per learner.
- It does not prove the same rate for all AI20k learners.
- It does not provide enough data to conclude the pain is only about lesson concepts rather than broader course support.
- It does not replace user validation interviews or a survey.

## Short Examples

Each quote is a short excerpt from the anonymized data pack and keeps the `msg_id` for reproducibility.

| msg_id | Pattern | Short excerpt |
|---|---|---|
| M13974 | lookup/status | `[@BOT] cho mình hỏi việc mình được điểm danh hay chưa có thể check ở đâu ạ` |
| M19079 | learning material | `[@BOT] Record của những buổi workshop tối được lưu ở đâu?` |
| M89035 | assignment/platform | `[@BOT] Bài lab1 tôi clone code, không fork thì bị tính là fail rồi đúng không?` |
| M84993 | assignment/status | `[@BOT] check xem t đã nộp bài codelab chưa` |
| M01578 | ambiguous/platform | `[@BOT] main là link github của project của nhóm à` |
| M10902 | lookup/status | `[@BOT] check điểm bonus của mình thế nào` |
| M08310 | very short / ambiguous | `[@BOT] TẠO TICKET` |

## Reproduce

```powershell
python evidence/mine_discord.py
```

The command prints the full count summary and short examples. It does not copy the raw data pack into the repo.
