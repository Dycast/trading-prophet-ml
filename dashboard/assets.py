
# Common Stocks
# Stocks Categorized by Region/Country
STOCKS_BY_REGION = {
    "🇺🇸 USA (Tech)": ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "NFLX", "AMD", "INTC"],
    "🇺🇸 USA (Finance & Consumer)": ["JPM", "BAC", "V", "MA", "WMT", "KO", "DIS", "MCD", "PG", "GS"],
    "🇺🇸 USA (Energy & Ind.)": ["XOM", "CVX", "GE", "HON", "CAT", "BA", "MMM", "LMT", "COP", "MPC"],
    "🇺🇸 USA (ETFs)": ["SPY", "QQQ", "DIA", "IWM", "GLD", "SLV", "USO", "UNG", "TLT", "IEF"],
    "🇪🇺 Europe": ["ASML.AS", "SAP.DE", "MC.PA", "RYA.L", "AZN.L", "SHELL.L", "BP.L", "NESN.SW", "NOVN.SW", "SIE.DE"],
    "🌏 Asia": ["700.HK", "9988.HK", "1211.HK", "SONY", "TM", "HSBC", "HDB", "INFY", "6758.T", "9984.T"],
    "🇨🇦 Canada": ["SHOP", "RY", "TD", "ENB", "CNR", "CP", "BN", "BNS", "CNQ", "BMO"],
    "🇦🇺 Australia": ["BHP.AX", "CBA.AX", "CSL.AX", "NAB.AX", "WBC.AX", "ANZ.AX", "FMG.AX", "WOW.AX", "TLS.AX", "RIO.AX"]
}

# Maintain a flat list for backward compatibility or simple lookups if needed
STOCKS = [stock for region in STOCKS_BY_REGION.values() for stock in region]

# Common Cryptocurrencies (Binance Pair Format)
CRYPTO = [
    "BTC/USDT", "ETH/USDT", "BNB/USDT", "XRP/USDT", "ADA/USDT", "DOGE/USDT", "SOL/USDT", "MATIC/USDT",
    "DOT/USDT", "LTC/USDT", "TRX/USDT", "SHIB/USDT", "AVAX/USDT", "UNI/USDT", "ATOM/USDT", "LINK/USDT",
    "XMR/USDT", "ETC/USDT", "XLM/USDT", "BCH/USDT", "ALGO/USDT", "FIL/USDT", "NEAR/USDT", "VET/USDT",
    "ICP/USDT", "EOS/USDT", "SAND/USDT", "AAVE/USDT", "THETA/USDT", "MANA/USDT", "AXS/USDT", "FTM/USDT",
    "XTZ/USDT", "EGLD/USDT", "HBAR/USDT", "ZQS/USDT", "KCS/USDT", "NEO/USDT", "IOTA/USDT", "DASH/USDT",
    "MKR/USDT", "COMP/USDT", "SNX/USDT", "ZEC/USDT", "WAVES/USDT", "BAT/USDT", "ZIL/USDT", "ONE/USDT"
]

# Forex Pairs (Example)
FOREX = [
    "EURUSD=X", "JPY=X", "GBPUSD=X", "AUDUSD=X", "NZDUSD=X", "EURJPY=X", "GBPJPY=X", "EURGBP=X", "EURCHF=X"
]
