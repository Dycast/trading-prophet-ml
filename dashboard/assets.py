#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Asset lists for Trading Prophet ML dashboard."""

# Stocks Categorized by Region/Country
STOCKS_BY_REGION = {
    "USA (Tech)": ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "NFLX", "AMD", "INTC"],
    "USA (Finance & Consumer)": ["JPM", "BAC", "V", "MA", "WMT", "KO", "DIS", "MCD", "PG", "GS"],
    "USA (Energy & Ind.)": ["XOM", "CVX", "GE", "HON", "CAT", "BA", "MMM", "LMT", "COP", "MPC"],
    "USA (ETFs)": ["SPY", "QQQ", "DIA", "IWM", "GLD", "SLV", "USO", "UNG", "TLT", "IEF"],
    "UK": ["HSBC", "RYA.L", "AZN.L", "SHELL.L", "BP.L", "GSK.L"],
    "Germany": ["SAP.DE", "SIE.DE", "BMW.DE", "VOW3.DE", "DBK.DE"],
    "France": ["MC.PA", "OR.PA", "RMS.PA", "TTE.PA"],
    "Netherlands": ["ASML.AS", "ADYEN.AS", "PRX.AS"],
    "Switzerland": ["NESN.SW", "NOVN.SW", "ROG.SW"],
    "Japan": ["SONY", "TM", "6758.T", "9984.T", "7203.T", "8306.T", "6861.T", "7974.T", "4063.T"],
    "South Korea": ["005930.KS", "000660.KS", "035420.KS", "051910.KS", "005380.KS", "068270.KS"],
    "China": ["BABA", "TCEHY", "PDD", "JD", "BIDU", "NIO", "XPEV", "LI"],
    "Hong Kong": ["700.HK", "9988.HK", "1211.HK", "3690.HK", "0001.HK", "0005.HK", "2318.HK"],
    "Taiwan": ["TSM", "2330.TW", "2317.TW", "2454.TW", "2308.TW"],
    "India": ["HDB", "INFY", "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ITC.NS", "BHARTIARTL.NS"],
    "Singapore": ["D05.SI", "Z74.SI", "C6L.SI", "U11.SI", "O39.SI", "SE", "GRAB"],
    "Thailand": ["PTT.BK", "CPALL.BK", "AOT.BK", "BBL.BK", "SCB.BK"],
    "Malaysia": ["1155.KL", "MAYBANK.KL", "TENAGA.KL", "CIMB.KL", "PUBLIC.KL"],
    "Indonesia": ["BBCA.JK", "BMRI.JK", "BBRI.JK", "TLKM.JK", "ASII.JK"],
    "Philippines": ["SM.PS", "AC.PS", "BDO.PS", "JFC.PS", "ALI.PS"],
    "Vietnam": ["VNM.VN", "VIC.VN", "VHM.VN", "HPG.VN", "FPT.VN"],
    "Canada": ["SHOP", "RY", "TD", "ENB", "CNR", "CP", "BN", "BNS", "CNQ", "BMO"],
    "Australia": ["BHP.AX", "CBA.AX", "CSL.AX", "NAB.AX", "WBC.AX", "ANZ.AX", "FMG.AX", "WOW.AX", "TLS.AX", "RIO.AX"],
}

# Flat list for backward compatibility
STOCKS = [stock for region in STOCKS_BY_REGION.values() for stock in region]

# Cryptocurrencies (Binance format)
CRYPTO = [
    "BTC/USDT", "ETH/USDT", "BNB/USDT", "XRP/USDT", "ADA/USDT", "DOGE/USDT", "SOL/USDT", "MATIC/USDT",
    "DOT/USDT", "LTC/USDT", "TRX/USDT", "SHIB/USDT", "AVAX/USDT", "UNI/USDT", "ATOM/USDT", "LINK/USDT",
    "XMR/USDT", "ETC/USDT", "XLM/USDT", "BCH/USDT", "ALGO/USDT", "FIL/USDT", "NEAR/USDT", "VET/USDT",
    "ICP/USDT", "EOS/USDT", "SAND/USDT", "AAVE/USDT", "THETA/USDT", "MANA/USDT", "AXS/USDT", "FTM/USDT",
]

# Forex Pairs
FOREX_DISPLAY = {
    "EUR/USD": "EURUSD=X",
    "USD/JPY": "JPY=X",
    "GBP/USD": "GBPUSD=X",
    "AUD/USD": "AUDUSD=X",
    "NZD/USD": "NZDUSD=X",
    "EUR/JPY": "EURJPY=X",
    "GBP/JPY": "GBPJPY=X",
    "EUR/GBP": "EURGBP=X",
    "EUR/CHF": "EURCHF=X",
}

FOREX = list(FOREX_DISPLAY.values())
