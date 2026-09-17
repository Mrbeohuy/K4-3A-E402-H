# Discord Mining Method

## Dataset

- File local: `data/discord-pack/k4_messages.csv`
- Total rows: 1,092 messages
- Non-bot messages with non-empty content: 779
- Denominator for the main evidence count: 307 non-bot messages that mention `[@BOT]`

The raw data pack is not copied into this repo. The script reads it locally.

## Reproducible Command

```powershell
python evidence/mine_discord.py
```

## Include Rules

A row is included in the main denominator when:

- `is_bot == False`
- `mentions_bot == True`
- `content` is non-empty

This captures learner/community messages explicitly sent to the Discord assistant.

## Exclude Rules

- Bot-authored messages are excluded from the denominator.
- Empty content is excluded.
- System/private/deleted messages are already outside the provided pack according to `data/discord-pack/DATA_DICTIONARY.md`.
- The method does not infer real identity from `author`, `channel`, timestamp, or masked content.

## Pattern Rules

The script counts four reproducible keyword-based patterns:

- `info_lookup_or_status`: bot-directed questions containing lookup/status terms such as `ở đâu`, `xem`, `check`, `link`, `file`, `record`, `lịch`, `hạn`, `điểm danh`, `XP`.
- `learning_material_or_assignment`: bot-directed questions containing learning/material/platform terms such as `bài`, `lab`, `codelab`, `record`, `workshop`, `github`, `repo`, `project`, `phoenix`, `vlearn`, `slide`.
- `ambiguous_or_very_short`: bot-directed messages with <=5 normalized tokens or phrases such as `cái này`, `như nào`, `thế nào`, `ý tôi`.
- `reply_or_follow_up`: bot-directed messages that are replies or have `reply_to`.

These rules are simple and auditable. They are not a semantic classifier.

## Current Result

- Main denominator: 307 bot-directed non-bot messages.
- `info_lookup_or_status`: 147 / 307 = 47.88%.
- `learning_material_or_assignment`: 52 / 307 = 16.94%.
- `ambiguous_or_very_short`: 78 / 307 = 25.41%.
- `reply_or_follow_up`: 12 / 307 = 3.91%.

## Interpretation Limits

- This is Evidence B, not survey Evidence A.
- It supports the broader pain that learners ask Discord for authoritative course/status/material help.
- It is not enough to conclude exact minutes lost per learner.
- It is not enough to conclude the whole course population has the same distribution.
- It only weakly supports the narrower claim "questions about lesson concepts" because many Discord cases are onboarding/admin/platform questions.

Where the data is insufficient, the spec should say: **CHƯA CÓ DỮ LIỆU ĐỦ ĐỂ KẾT LUẬN**.
