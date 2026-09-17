import csv
import json
import re
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "data" / "discord-pack" / "k4_messages.csv"

INFO_LOOKUP_TERMS = (
    "bao nhieu",
    "check",
    "danh sach",
    "diem danh",
    "file",
    "han",
    "huong dan",
    "khi nao",
    "kiem tra",
    "lich",
    "link",
    "luu o dau",
    "o dau",
    "record",
    "setup",
    "xem",
    "xp",
)

LEARNING_MATERIAL_TERMS = (
    "bai",
    "codelab",
    "github",
    "lab",
    "lecture",
    "phoenix",
    "project",
    "record",
    "repo",
    "setup",
    "slide",
    "vlearn",
    "workshop",
)

AMBIGUOUS_TERMS = (
    "cai nay",
    "nhu nao",
    "the nao",
    "y toi",
)


def normalize(text):
    text = text.lower().replace("đ", "d")
    text = unicodedata.normalize("NFD", text)
    text = "".join(char for char in text if unicodedata.category(char) != "Mn")
    return re.sub(r"\s+", " ", text).strip()


def tokens(text):
    return re.findall(r"[a-z0-9]+", normalize(text))


def is_true(value):
    return str(value).strip().lower() == "true"


def short_excerpt(text, max_chars=160):
    compact = re.sub(r"\s+", " ", text).strip()
    if len(compact) <= max_chars:
        return compact
    return compact[: max_chars - 3].rstrip() + "..."


def has_any(normalized_text, terms):
    return any(term in normalized_text for term in terms)


def row_to_example(row):
    return {
        "msg_id": row["msg_id"],
        "created_at_vn": row["created_at_vn"],
        "channel": row["channel"],
        "excerpt": short_excerpt(row["content"]),
    }


def mine_rows(rows):
    non_bot = [row for row in rows if not is_true(row["is_bot"]) and row["content"].strip()]
    bot_directed = [row for row in non_bot if is_true(row["mentions_bot"])]

    info_lookup = []
    material_lookup = []
    ambiguous_or_short = []
    follow_up = []

    for row in bot_directed:
        text = normalize(row["content"])
        row_tokens = tokens(row["content"])
        if has_any(text, INFO_LOOKUP_TERMS):
            info_lookup.append(row)
        if has_any(text, LEARNING_MATERIAL_TERMS):
            material_lookup.append(row)
        if len(row_tokens) <= 5 or has_any(text, AMBIGUOUS_TERMS):
            ambiguous_or_short.append(row)
        if row["msg_type"] == "reply" or row["reply_to"].strip():
            follow_up.append(row)

    return {
        "dataset": str(DATASET.relative_to(ROOT)).replace("\\", "/"),
        "total_rows": len(rows),
        "non_bot_messages": len(non_bot),
        "bot_directed_non_bot_messages": len(bot_directed),
        "patterns": {
            "info_lookup_or_status": {
                "count": len(info_lookup),
                "percentage_of_bot_directed": round(len(info_lookup) / len(bot_directed) * 100, 2)
                if bot_directed
                else 0,
                "examples": [row_to_example(row) for row in info_lookup[:6]],
            },
            "learning_material_or_assignment": {
                "count": len(material_lookup),
                "percentage_of_bot_directed": round(len(material_lookup) / len(bot_directed) * 100, 2)
                if bot_directed
                else 0,
                "examples": [row_to_example(row) for row in material_lookup[:6]],
            },
            "ambiguous_or_very_short": {
                "count": len(ambiguous_or_short),
                "percentage_of_bot_directed": round(
                    len(ambiguous_or_short) / len(bot_directed) * 100, 2
                )
                if bot_directed
                else 0,
                "examples": [row_to_example(row) for row in ambiguous_or_short[:6]],
            },
            "reply_or_follow_up": {
                "count": len(follow_up),
                "percentage_of_bot_directed": round(len(follow_up) / len(bot_directed) * 100, 2)
                if bot_directed
                else 0,
                "examples": [row_to_example(row) for row in follow_up[:6]],
            },
        },
    }


def main():
    with DATASET.open("r", encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file))
    print(json.dumps(mine_rows(rows), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
