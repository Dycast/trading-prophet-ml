#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dashboard component helpers with flag emoji support."""
from __future__ import annotations

import re
from typing import Optional

from dashboard.assets import STOCKS_BY_REGION, CRYPTO, FOREX_DISPLAY


def extract_flag(text: str) -> str:
    """Extract flag emoji from region/pair text.
    
    Examples:
        "🇺🇸 USA (Tech)" -> "🇺🇸"
        "🪙 BTC/USDT" -> "🪙"
        "NVDA" -> "🔍"
    """
    match = re.match(r'^(\S+)', text)
    if match:
        extracted = match.group(1)
        if len(extracted) > 0 and ord(extracted[0]) > 127:  # Unicode character
            return extracted
    return "🔍"


def get_stock_display_name(region: str, stock: str) -> str:
    """Get stock display name with flag."""
    flag = extract_flag(region)
    return f"{flag} {stock}"


def get_crypto_display_name(pair: str) -> str:
    """Get crypto display name with emoji."""
    return f"🪙 {pair}"


def get_forex_display_options() -> list[str]:
    """Get formatted forex pair options with flags."""
    return list(FOREX_DISPLAY.keys())


def extract_symbol_from_display(display_text: str) -> str:
    """Extract the actual symbol from display text.
    
    Examples:
        "🇺🇸 AAPL" -> "AAPL"
        "🪙 BTC/USDT" -> "BTC/USDT"
    """
    # Split on space and take the last part
    parts = display_text.split()
    return parts[-1] if parts else display_text


def get_all_regions() -> list[str]:
    """Get all region options with flag emojis."""
    return list(STOCKS_BY_REGION.keys())


def get_stocks_for_region(region: str) -> list[str]:
    """Get stocks for a specific region."""
    return STOCKS_BY_REGION.get(region, [])


def get_all_crypto() -> list[str]:
    """Get all crypto pairs."""
    return CRYPTO


def format_region_header(region: str) -> str:
    """Format region text for display (with flag and label)."""
    return region  # Already formatted with flag in assets.py
