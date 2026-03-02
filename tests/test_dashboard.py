#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test dashboard assets."""
from dashboard.assets import STOCKS_BY_REGION, CRYPTO, FOREX_DISPLAY


def test_stock_regions():
    """Test that stock regions are loaded correctly."""
    assert len(STOCKS_BY_REGION) > 0, "Should have stock regions"
    for region, stocks in STOCKS_BY_REGION.items():
        assert isinstance(region, str), "Region should be string"
        assert isinstance(stocks, list), "Stocks should be list"
        assert len(stocks) > 0, f"Region '{region}' should have stocks"
    print(f"✓ {len(STOCKS_BY_REGION)} stock regions loaded")


def test_crypto_list():
    """Test that crypto list is loaded."""
    assert len(CRYPTO) > 0, "Should have crypto pairs"
    assert all("/" in c for c in CRYPTO), "Crypto should be in PAIR/USDT format"
    print(f"✓ {len(CRYPTO)} crypto pairs available")


def test_forex_display():
    """Test that forex pairs are loaded."""
    assert len(FOREX_DISPLAY) > 0, "Should have forex pairs"
    for display_name, symbol in FOREX_DISPLAY.items():
        assert isinstance(display_name, str), "Display name should be string"
        assert isinstance(symbol, str), "Symbol should be string"
    print(f"✓ {len(FOREX_DISPLAY)} forex pairs loaded")


if __name__ == "__main__":
    test_stock_regions()
    test_crypto_list()
    test_forex_display()
    print("\n✅ All dashboard tests passed!")

