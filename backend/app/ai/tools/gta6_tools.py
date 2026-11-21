"""Gemini tools for GTA 6, backed by the gta6_* MySQL tables (db/init/02_gta6.sql)."""
import re
from typing import Any

from db.gta6_queries import get_all_rows, get_facts

FACT_TOPICS = (
    "release", "platforms", "delays", "performance",
    "reviews", "sales", "online", "preorder_bonus", "marketing",
)


def _norm(text: str | None) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (text or "").lower()).strip()


def _clean(row: dict) -> dict:
    """Drop internal columns and empty values; MySQL returns BOOLEAN as 0/1."""
    out = {k: v for k, v in row.items() if k not in ("id", "aliases") and v not in (None, "")}
    if "playable" in out:
        out["playable"] = bool(out["playable"])
    return out


def _find(rows: list[dict], name: str | None) -> dict | None:
    """Match on full name or alias first, then on a partial name."""
    wanted = _norm(name)
    if not wanted:
        return None
    for row in rows:
        aliases = [_norm(a) for a in (row.get("aliases") or "").split(",")]
        if wanted == _norm(row["name"]) or wanted in aliases:
            return row
    for row in rows:
        if wanted in _norm(row["name"]) or _norm(row["name"]) in wanted:
            return row
    return None


def get_character(name: str | None) -> dict[str, Any]:
    rows = get_all_rows("gta6_characters")
    match = _find(rows, name)
    if match is None:
        return {"error": f"No GTA 6 character found for {name!r}.",
                "available_characters": [r["name"] for r in rows]}
    return {"character": _clean(match)}


def get_region(name: str | None) -> dict[str, Any]:
    rows = get_all_rows("gta6_regions")
    match = _find(rows, name)
    if match is None:
        return {"error": f"No Leonida region found for {name!r}.",
                "available_regions": [r["name"] for r in rows]}
    return {"region": _clean(match)}


def compare_editions() -> dict[str, Any]:
    return {
        "editions": [_clean(r) for r in get_all_rows("gta6_editions")],
        "preorder_bonus": {f["fact_key"]: f["fact_value"] for f in get_facts("preorder_bonus")},
    }


def get_game_facts(topic: str | None) -> dict[str, Any]:
    topic = _norm(topic).replace(" ", "_")
    if topic not in FACT_TOPICS:
        return {"error": f"Unknown topic {topic!r}.", "available_topics": list(FACT_TOPICS)}
    return {"topic": topic, "facts": {f["fact_key"]: f["fact_value"] for f in get_facts(topic)}}
