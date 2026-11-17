from datetime import datetime, timezone


def utc_now_iso() -> str:
    """Current time in UTC as ISO 8601, e.g. 2026-11-17T05:39:12+00:00."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")
