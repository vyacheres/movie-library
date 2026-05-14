"""Простое ограничение частоты запросов к /login по IP (in-memory)."""

from collections import defaultdict
from time import monotonic

from fastapi import HTTPException, Request, status

_window_sec = 60.0
_max_attempts = 30
_buckets: dict[str, list[float]] = defaultdict(list)


def enforce_login_rate_limit(request: Request) -> None:
    host = request.client.host if request.client else "unknown"
    now = monotonic()
    bucket = _buckets[host]
    bucket[:] = [t for t in bucket if now - t < _window_sec]
    if len(bucket) >= _max_attempts:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many login attempts. Try again later.",
        )
    bucket.append(now)
