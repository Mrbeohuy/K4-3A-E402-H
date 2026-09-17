import csv
import re
import unicodedata
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
DATA_ROOT = PROJECT_ROOT / "data"
VLEARN_ROOT = DATA_ROOT / "vlearn-pack"
DISCORD_ROOT = DATA_ROOT / "discord-pack"

MAX_CONTENT_CHARS = 1200
DEFAULT_TOP_K = 5
MIN_RETRIEVAL_SCORE = 1.8

QUERY_ALIASES = {
    "llm": ("mo", "hinh", "ngon", "ngu", "lon"),
    "attention": ("chu",),
}

DEFINITION_MARKERS = (
    " la ",
    " la mot ",
    " co nghia la ",
    " duoc goi la ",
    " goi la ",
    " don vi ",
    " thuat ngu ",
    " can nam duoc ",
    " khong phai ",
)

STRONG_DEFINITION_MARKERS = (
    " co nghia la ",
    " don vi ",
    " thuat ngu ",
    " can nam duoc ",
)

STOPWORDS = {
    "a",
    "ai",
    "anh",
    "au",
    "activity",
    "ban",
    "bang",
    "bat",
    "bai",
    "bi",
    "biet",
    "buoc",
    "cai",
    "cac",
    "ca",
    "can",
    "cho",
    "chua",
    "chuong",
    "co",
    "con",
    "cua",
    "da",
    "de",
    "di",
    "duoc",
    "danh",
    "dau",
    "diem",
    "discord",
    "do",
    "gi",
    "giup",
    "giang",
    "giong",
    "github",
    "hang",
    "hay",
    "hoac",
    "hoc",
    "hoi",
    "hom",
    "huong",
    "kenh",
    "khac",
    "khai",
    "khi",
    "khong",
    "khoa",
    "la",
    "lai",
    "lam",
    "level",
    "lich",
    "link",
    "lop",
    "main",
    "minh",
    "moi",
    "mot",
    "muon",
    "nao",
    "nay",
    "nen",
    "nhu",
    "nhau",
    "nhan",
    "nhom",
    "noi",
    "o",
    "phan",
    "project",
    "sao",
    "su",
    "tai",
    "the",
    "thi",
    "thich",
    "thieu",
    "thay",
    "to",
    "toi",
    "trinh",
    "trong",
    "tren",
    "tu",
    "va",
    "ve",
    "viec",
    "vien",
    "voi",
    "dan",
    "giai",
    "gioi",
}

CHATLOG_KEYWORDS = (
    "ai",
    "agent",
    "api",
    "assignment",
    "bot",
    "deadline",
    "discord",
    "gemini",
    "github",
    "hackathon",
    "llm",
    "mentor",
    "prompt",
    "react",
    "repo",
    "standup",
    "token",
)


@dataclass(frozen=True)
class ScoredSource:
    source: dict
    score: float


def _strip_accents(text):
    text = text.lower().replace("\u0111", "d").replace("\u0110", "d")
    normalized = unicodedata.normalize("NFD", text)
    return "".join(char for char in normalized if unicodedata.category(char) != "Mn")


def _tokens(text):
    normalized = _strip_accents(text.replace("_", " "))
    return [
        token
        for token in re.findall(r"[a-z0-9]+", normalized)
        if len(token) > 1 and token not in STOPWORDS
    ]


def _unique_tokens(tokens):
    seen = set()
    unique = []
    for token in tokens:
        if token in seen:
            continue
        seen.add(token)
        unique.append(token)
    return unique


def _expanded_query_tokens(tokens):
    expanded = []
    for token in tokens:
        expanded.append(token)
        expanded.extend(QUERY_ALIASES.get(token, ()))
    return _unique_tokens(
        token for token in expanded if len(token) > 1 and token not in STOPWORDS
    )


def _shorten(text, max_chars=MAX_CONTENT_CHARS):
    compact = re.sub(r"\s+", " ", text).strip()
    if len(compact) <= max_chars:
        return compact
    return compact[: max_chars - 3].rstrip() + "..."


def _make_source(source_id, title, provenance, content):
    return {
        "id": source_id,
        "title": title,
        "provenance": provenance,
        "content": _shorten(content),
    }


def _load_transcript_sources():
    transcript_dir = VLEARN_ROOT / "transcript"
    if not transcript_dir.exists():
        return []

    sources = []
    pattern = re.compile(r"^\*\*\[(T\d{2})-(\d{3})\]\*\*\s*(.*)$")
    for path in sorted(transcript_dir.glob("transcript-*-clean.md")):
        text = path.read_text(encoding="utf-8")
        current_code = None
        current_number = None
        current_lines = []

        def flush():
            if not current_code or not current_lines:
                return
            source_id = f"VLEARN_{current_code}_SEG_{current_number}"
            title = f"VLearn transcript {current_code}-{current_number}"
            provenance = f"data/vlearn-pack/transcript/{path.name}#[{current_code}-{current_number}]"
            sources.append(_make_source(source_id, title, provenance, "\n".join(current_lines)))

        for line in text.splitlines():
            match = pattern.match(line.strip())
            if match:
                flush()
                current_code = match.group(1)
                current_number = match.group(2)
                current_lines = [match.group(3).strip()]
            elif current_code:
                current_lines.append(line.strip())
        flush()
    return sources


def _load_pdf_slide_sources():
    slide_dir = VLEARN_ROOT / "slides"
    if not slide_dir.exists():
        return []

    try:
        from pypdf import PdfReader
    except ImportError:
        return []

    sources = []
    for path in sorted(slide_dir.glob("*.pdf")):
        day_match = re.search(r"d(\d+)-", path.name.lower())
        day_label = f"DAY{day_match.group(1)}" if day_match else path.stem.upper()
        reader = PdfReader(str(path))
        for index, page in enumerate(reader.pages, start=1):
            content = _shorten(page.extract_text() or "", max_chars=MAX_CONTENT_CHARS)
            if not content:
                continue
            source_id = f"VLEARN_{day_label}_SLIDE_{index:03d}"
            title = f"VLearn {day_label} slide {index:03d}"
            provenance = f"data/vlearn-pack/slides/{path.name}#page={index}"
            sources.append(_make_source(source_id, title, provenance, content))
    return sources


@lru_cache(maxsize=1)
def load_vlearn_sources_cached():
    return tuple(_load_transcript_sources() + _load_pdf_slide_sources())


def load_vlearn_sources():
    return [dict(source) for source in load_vlearn_sources_cached()]


def _source_score(query_tokens, query_text, source):
    if not query_tokens:
        return 0.0
    original_query_tokens = _unique_tokens(_tokens(query_text))

    source_text = f"{source['title']} {source['content']}"
    source_tokens = _tokens(source_text)
    if not source_tokens:
        return 0.0

    token_counts = {}
    for token in source_tokens:
        token_counts[token] = token_counts.get(token, 0) + 1

    matched_query_tokens = [token for token in query_tokens if token in token_counts]
    if len(query_tokens) >= 2 and len(set(matched_query_tokens)) < 2:
        return 0.0

    score = 0.0
    for token in matched_query_tokens:
        weight = 1.0 if token in original_query_tokens else 0.45
        score += weight * (1.0 + min(token_counts[token], 3) * 0.25)

    matched_original_tokens = [
        token for token in original_query_tokens if token in token_counts
    ]
    if len(original_query_tokens) >= 2 and len(set(matched_original_tokens)) >= 2:
        score += 4.0
    elif matched_original_tokens:
        score += 1.0

    normalized_source = _strip_accents(source_text)
    normalized_query = _strip_accents(query_text)
    if normalized_query and normalized_query in normalized_source:
        score += 4.0

    for left, right in zip(query_tokens, query_tokens[1:]):
        phrase = f"{left} {right}"
        if phrase in normalized_source:
            score += 1.5

    score += _proximity_score(query_tokens, source_tokens)
    score += _definition_score(query_tokens, normalized_source)

    if "data/vlearn-pack/transcript/" in source.get("provenance", ""):
        score += 0.2

    return score


def _proximity_score(query_tokens, source_tokens):
    wanted = set(query_tokens)
    if len(wanted) < 2:
        return 0.0

    positions = [
        (index, token) for index, token in enumerate(source_tokens) if token in wanted
    ]
    best_window = None
    for left_index, (left_position, left_token) in enumerate(positions):
        seen = {left_token}
        for right_position, right_token in positions[left_index + 1 :]:
            seen.add(right_token)
            if len(seen) >= 2:
                window = right_position - left_position
                if best_window is None or window < best_window:
                    best_window = window
                break

    if best_window is None:
        return 0.0
    if best_window <= 8:
        return 2.5
    if best_window <= 20:
        return 1.5
    if best_window <= 40:
        return 0.75
    return 0.0


def _definition_score(query_tokens, normalized_source):
    best = 0.0
    for sentence in re.split(r"[\n.!?]+", normalized_source):
        if not sentence.strip():
            continue
        matched_terms = [
            token
            for token in query_tokens
            if re.search(rf"\b{re.escape(token)}\b", sentence)
        ]
        if not matched_terms:
            continue
        padded_sentence = f" {sentence} "
        if any(marker in padded_sentence for marker in DEFINITION_MARKERS):
            marker_bonus = 1.0
            if any(marker in padded_sentence for marker in STRONG_DEFINITION_MARKERS):
                marker_bonus += 2.0
            best = max(best, marker_bonus + min(len(set(matched_terms)), 3) * 0.6)
    return best


def retrieve_sources(question, top_k=DEFAULT_TOP_K):
    query_tokens = _expanded_query_tokens(_tokens(question))
    if not query_tokens:
        return []

    scored = [
        ScoredSource(source=source, score=_source_score(query_tokens, question, source))
        for source in load_vlearn_sources()
    ]
    relevant = [item for item in scored if item.score >= MIN_RETRIEVAL_SCORE]
    relevant.sort(key=lambda item: (-item.score, item.source["id"]))
    return [dict(item.source) for item in relevant[:top_k]]


def load_discord_golden_candidates(limit=10):
    path = DISCORD_ROOT / "k4_messages.csv"
    if not path.exists():
        return []

    candidates = []
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if str(row.get("is_bot", "")).strip().lower() == "true":
                continue
            content = str(row.get("content", "")).strip()
            if not content:
                continue
            normalized = _strip_accents(content)
            mentions_bot = str(row.get("mentions_bot", "")).strip().lower() == "true"
            looks_like_question = "?" in content or any(keyword in normalized for keyword in CHATLOG_KEYWORDS)
            if not mentions_bot and not looks_like_question:
                continue
            tokens = _tokens(content)
            if len(tokens) < 2:
                continue
            candidates.append(
                {
                    "msg_id": row.get("msg_id", ""),
                    "channel": row.get("channel", ""),
                    "created_at_vn": row.get("created_at_vn", ""),
                    "excerpt": _shorten(content, max_chars=180),
                }
            )
            if len(candidates) >= limit:
                break
    return candidates
