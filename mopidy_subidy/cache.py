import json
import logging
import time
from pathlib import Path

logger = logging.getLogger(__name__)

CACHE_FILENAME = "subidy_cache.json"


class SubidyCache:
    """Small in-memory TTL cache for subsonic API responses, optionally
    persisted to disk between mopidy restarts."""

    def __init__(self, cache_dir=None, ttl=3600):
        self.ttl = ttl
        self.cache_file = (
            Path(cache_dir) / CACHE_FILENAME if cache_dir else None
        )
        self.store = {}
        self._load()

    def _key(self, method_name, args):
        return f"{method_name}|{args!r}"

    def get_or_fetch(self, method_name, args, fetch_fn):
        key = self._key(method_name, args)
        now = time.time()
        entry = self.store.get(key)
        if entry is not None and now - entry[0] < self.ttl:
            logger.info("Subidy cache hit for %s%s", method_name, args)
            return entry[1]

        start = time.monotonic()
        result = fetch_fn()
        elapsed_ms = (time.monotonic() - start) * 1000
        logger.info(
            "Subidy cache miss for %s%s, fetched in %.1fms",
            method_name,
            args,
            elapsed_ms,
        )
        self.store[key] = (now, result)
        return result

    def invalidate(self, method_name, args=None):
        if args is not None:
            self.store.pop(self._key(method_name, args), None)
            return
        prefix = f"{method_name}|"
        for key in [k for k in self.store if k.startswith(prefix)]:
            del self.store[key]

    def _load(self):
        if self.cache_file is None or not self.cache_file.exists():
            return
        try:
            with open(self.cache_file) as f:
                raw = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            logger.warning("Could not load subidy cache from disk: %s", e)
            return
        now = time.time()
        loaded = 0
        for key, (timestamp, value) in raw.items():
            if now - timestamp < self.ttl:
                self.store[key] = (timestamp, value)
                loaded += 1
        logger.info(
            "Loaded %d cached subidy response(s) from %s",
            loaded,
            self.cache_file,
        )

    def save(self):
        if self.cache_file is None:
            return
        try:
            self.cache_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.cache_file, "w") as f:
                json.dump(self.store, f)
            logger.info(
                "Persisted %d cached subidy response(s) to %s",
                len(self.store),
                self.cache_file,
            )
        except OSError as e:
            logger.warning("Could not persist subidy cache to disk: %s", e)
