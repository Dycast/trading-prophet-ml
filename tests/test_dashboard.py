#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test dashboard assets and components."""
from dashboard.assets import STOCKS_BY_REGION, CRYPTO, FOREX_DISPLAY
from dashboard.components import extract_flag, extract_symbol_from_display


def test_flag_extraction():
    """Test that flags extract correctly."""
    assert extract_flag("🇺🇸 USA (Tech)") == "🇺🇸"
    assert extract_flag("🪙 BTC/USDT") == "🪙"
    assert extract_flag("🇬🇧 UK") == "🇬🇧"
    print("✓ Flag extraction works")


def test_symbol_extraction():
    """Test that symbols extract correctly from display text."""
    assert extract_symbol_from_display("🇺🇸 AAPL") == "AAPL"
    assert extract_symbol_from_display("🪙 BTC/USDT") == "BTC/USDT"
    print("✓ Symbol extraction works")


def test_stock_regions():
    """Test that stock regions have flags."""
    regions = list(STOCKS_BY_REGION.keys())
    assert len(regions) > 0
    for region in regions:
        flag = extract_flag(region)
        assert flag != "🔍", f"Region '{region}' has no flag"
    print(f"✓ All {len(regions)} stock regions have flags")


def test_crypto_list():
    """Test crypto list."""
    assert len(CRYPTO) > 0
    print(f"✓ {len(CRYPTO)} crypto pairs available")


def test_forex_display():
    """Test forex pairs with flags."""
    pairs = list(FOREX_DISPLAY.keys())
    assert len(pairs) > 0
    for pair in pairs:
        flag = extract_flag(pair)
        assert flag != "🔍", f"Pair '{pair}' has no flag"
    print(f"✓ All {len(pairs)} forex pairs have flags")


if __name__ == "__main__":
    test_flag_extraction()
    test_symbol_extraction()
    test_stock_regions()
    test_crypto_list()
    test_forex_display()
    print("\n✅ All dashboard component tests passed!")
