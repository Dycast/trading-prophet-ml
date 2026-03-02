"""Service layer for API and dashboard."""
from __future__ import annotations

from typing import Any
from pathlib import Path

import pandas as pd

from .data.data_fetcher import DataFetcher
from .data.data_manager import DataManager
from .data.data_preprocessor import adjust_for_splits_dividends, handle_missing
from .config_loader import load_yaml
from .news import fetch_latest_news
from .pipeline import run_quick_analysis
from .predictor import naive_linear_forecast


def analyze_asset(
    asset: str,
    timeframe: str = "1d",
    period: str = "1y",
    *,
    force_refresh: bool | None = None,
    max_cache_age_seconds: int | None = None,
) -> dict[str, Any]:
    return run_quick_analysis(
        asset=asset,
        timeframe=timeframe,
        period=period,
        force_refresh=force_refresh,
        max_cache_age_seconds=max_cache_age_seconds,
    )


def predict_asset(
    asset: str,
    timeframe: str = "1d",
    period: str = "1y",
    horizon: int = 1,
    *,
    force_refresh: bool | None = None,
    max_cache_age_seconds: int | None = None,
) -> dict[str, Any]:
    fetcher = DataFetcher()
    manager = DataManager("data")
    config = load_yaml(Path("config") / "config.yaml")
    data_cfg = config.get("data", {})

    if force_refresh is None:
        force_refresh = bool(data_cfg.get("force_refresh", True))
    if max_cache_age_seconds is None:
        max_cache_age_seconds = data_cfg.get("max_cache_age_seconds", 60)

    cache_key = f"{asset}-{timeframe}-{period}"

    def _fetch():
        if "/" in asset:
            return fetcher.fetch_ccxt("binance", asset, timeframe)
        return fetcher.fetch_yfinance(asset, interval=timeframe, period=period)

    df = manager.get_or_fetch(
        cache_key,
        _fetch,
        max_age_seconds=max_cache_age_seconds,
        force_refresh=force_refresh,
    )
    df = adjust_for_splits_dividends(df)
    df = handle_missing(df)

    result = naive_linear_forecast(df, horizon=horizon)

    latest_timestamp = None
    if not df.empty:
        idx = df.index[-1]
        try:
            latest_timestamp = pd.to_datetime(idx, utc=True).isoformat()
        except Exception:  # noqa: BLE001
            latest_timestamp = str(idx)

    return {
        "prediction": result.prediction,
        "confidence": result.confidence,
        "method": result.method,
        "findings": result.findings,
        "data_last_updated": latest_timestamp,
        "latest_news": fetch_latest_news(asset),
        "disclaimer": "Not financial advice.",
    }
