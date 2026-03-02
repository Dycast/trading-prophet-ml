"""Latest news retrieval for assets."""
from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any


def _to_iso_utc(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value, tz=timezone.utc).isoformat()
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return None
        try:
            if text.endswith("Z"):
                return datetime.fromisoformat(text.replace("Z", "+00:00")).astimezone(timezone.utc).isoformat()
            return datetime.fromisoformat(text).astimezone(timezone.utc).isoformat()
        except ValueError:
            return text
    return None


def _asset_query(asset: str) -> str:
    if "/" in asset:
        base, quote = asset.split("/", 1)
        return f"{base} {quote} crypto"
    if asset.endswith("=X") and len(asset) >= 6:
        return f"{asset.replace('=X', '')} forex"
    return asset


def fetch_latest_news(asset: str, max_items: int = 8) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []

    try:
        import yfinance as yf

        if "/" not in asset and not asset.endswith("=X"):
            ticker = yf.Ticker(asset)
            for entry in (ticker.news or [])[: max_items * 2]:
                link = entry.get("link") or entry.get("url")
                title = entry.get("title")
                if not title or not link:
                    continue
                items.append(
                    {
                        "title": title,
                        "source": entry.get("publisher") or "Yahoo Finance",
                        "url": link,
                        "published_at": _to_iso_utc(entry.get("providerPublishTime") or entry.get("published_at")),
                    }
                )
    except Exception:
        pass

    api_key = os.getenv("NEWS_API_KEY") or os.getenv("NEWSAPI_KEY")
    if api_key:
        try:
            import requests

            response = requests.get(
                "https://newsapi.org/v2/everything",
                params={
                    "q": _asset_query(asset),
                    "sortBy": "publishedAt",
                    "language": "en",
                    "pageSize": max_items,
                    "apiKey": api_key,
                },
                timeout=15,
            )
            response.raise_for_status()
            payload = response.json()
            for article in payload.get("articles", [])[:max_items]:
                title = article.get("title")
                url = article.get("url")
                if not title or not url:
                    continue
                items.append(
                    {
                        "title": title,
                        "source": (article.get("source") or {}).get("name") or "NewsAPI",
                        "url": url,
                        "published_at": _to_iso_utc(article.get("publishedAt")),
                    }
                )
        except Exception:
            pass

    deduped: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in items:
        key = f"{item.get('title', '')}|{item.get('url', '')}".strip().lower()
        if not key or key in seen:
            continue
        seen.add(key)
        deduped.append(item)

    def _sort_key(entry: dict[str, Any]) -> str:
        return entry.get("published_at") or ""

    deduped.sort(key=_sort_key, reverse=True)
    return deduped[:max_items]
