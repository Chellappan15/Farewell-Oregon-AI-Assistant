import logging
import time

logger = logging.getLogger("chat.timing")


class RequestTimer:
    """Collects per-stage timings for one chat request and logs them as one line.

    Example log line:
    chat_request game=gta6 mode=hybrid stream=True status=ok history_ms=12 retrieval_ms=184
    first_token_ms=903 llm_ms=2410 tool_rounds=1 total_ms=2611
    """

    def __init__(self, **fields):
        self._start = time.perf_counter()
        self._mark = self._start
        self.fields = dict(fields)
        self.fields.setdefault("status", "ok")
        self.fields.setdefault("tool_rounds", 0)

    def lap(self, name: str) -> None:
        """Record the time since the previous lap under <name>_ms."""
        now = time.perf_counter()
        self.fields[f"{name}_ms"] = round((now - self._mark) * 1000)
        self._mark = now

    def since_start(self, name: str) -> None:
        """Record the time since the request started under <name>_ms (no lap reset)."""
        self.fields.setdefault(f"{name}_ms", round((time.perf_counter() - self._start) * 1000))

    def log(self) -> None:
        self.fields["total_ms"] = round((time.perf_counter() - self._start) * 1000)
        logger.info("chat_request " + " ".join(f"{k}={v}" for k, v in self.fields.items()))
