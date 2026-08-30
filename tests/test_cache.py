import time

from mopidy_subidy.cache import SubidyCache


def make_counter():
    calls = {"n": 0}

    def fetch():
        calls["n"] += 1
        return {"call": calls["n"]}

    return calls, fetch


def test_miss_then_hit_does_not_refetch():
    cache = SubidyCache(cache_dir=None, ttl=60)
    calls, fetch = make_counter()

    first = cache.get_or_fetch("getFoo", ("a",), fetch)
    second = cache.get_or_fetch("getFoo", ("a",), fetch)

    assert calls["n"] == 1
    assert first == second == {"call": 1}


def test_different_args_are_different_cache_entries():
    cache = SubidyCache(cache_dir=None, ttl=60)
    calls, fetch = make_counter()

    cache.get_or_fetch("getFoo", ("a",), fetch)
    cache.get_or_fetch("getFoo", ("b",), fetch)

    assert calls["n"] == 2


def test_entry_expires_after_ttl():
    cache = SubidyCache(cache_dir=None, ttl=0.05)
    calls, fetch = make_counter()

    cache.get_or_fetch("getFoo", ("a",), fetch)
    time.sleep(0.1)
    cache.get_or_fetch("getFoo", ("a",), fetch)

    assert calls["n"] == 2


def test_invalidate_specific_args_only_clears_that_entry():
    cache = SubidyCache(cache_dir=None, ttl=60)
    calls, fetch = make_counter()

    cache.get_or_fetch("getFoo", ("a",), fetch)
    cache.get_or_fetch("getFoo", ("b",), fetch)
    cache.invalidate("getFoo", ("a",))

    cache.get_or_fetch("getFoo", ("a",), fetch)
    cache.get_or_fetch("getFoo", ("b",), fetch)

    assert calls["n"] == 3


def test_invalidate_without_args_clears_all_entries_for_method():
    cache = SubidyCache(cache_dir=None, ttl=60)
    calls, fetch = make_counter()

    cache.get_or_fetch("getFoo", ("a",), fetch)
    cache.get_or_fetch("getFoo", ("b",), fetch)
    cache.invalidate("getFoo")

    cache.get_or_fetch("getFoo", ("a",), fetch)
    cache.get_or_fetch("getFoo", ("b",), fetch)

    assert calls["n"] == 4


def test_invalidate_does_not_affect_other_methods():
    cache = SubidyCache(cache_dir=None, ttl=60)
    calls, fetch = make_counter()

    cache.get_or_fetch("getFoo", ("a",), fetch)
    cache.invalidate("getBar")
    cache.get_or_fetch("getFoo", ("a",), fetch)

    assert calls["n"] == 1


def test_persists_and_reloads_from_disk(tmp_path):
    calls, fetch = make_counter()

    cache = SubidyCache(cache_dir=tmp_path, ttl=60)
    cache.get_or_fetch("getFoo", ("a",), fetch)
    cache.save()

    reloaded = SubidyCache(cache_dir=tmp_path, ttl=60)
    reloaded.get_or_fetch("getFoo", ("a",), fetch)

    assert calls["n"] == 1


def test_does_not_reload_expired_entries_from_disk(tmp_path):
    calls, fetch = make_counter()

    cache = SubidyCache(cache_dir=tmp_path, ttl=0.05)
    cache.get_or_fetch("getFoo", ("a",), fetch)
    cache.save()
    time.sleep(0.1)

    reloaded = SubidyCache(cache_dir=tmp_path, ttl=0.05)
    reloaded.get_or_fetch("getFoo", ("a",), fetch)

    assert calls["n"] == 2


def test_no_cache_dir_skips_persistence(tmp_path):
    cache = SubidyCache(cache_dir=None, ttl=60)
    cache.get_or_fetch("getFoo", ("a",), lambda: {"ok": True})

    cache.save()

    assert list(tmp_path.iterdir()) == []
