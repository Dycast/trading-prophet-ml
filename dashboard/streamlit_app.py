"""Streamlit dashboard for Trading Prophet ML."""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from dashboard.assets import STOCKS, STOCKS_BY_REGION, CRYPTO, FOREX, FOREX_DISPLAY
from src.config_loader import load_yaml
from src.service import analyze_asset, predict_asset


_APP_CONFIG = load_yaml(Path("config") / "config.yaml")
_DASH_CACHE_TTL = int(_APP_CONFIG.get("dashboard", {}).get("cache_ttl_seconds", 30))


# Custom layout configuration
st.set_page_config(
    page_title="Trading Prophet ML",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data(ttl=_DASH_CACHE_TTL)
def cached_analysis(asset: str, timeframe: str, period: str) -> dict:
    try:
        return analyze_asset(asset, timeframe, period)
    except Exception as e:
        return {"error": str(e)}


@st.cache_data(ttl=_DASH_CACHE_TTL)
def cached_prediction(asset: str, timeframe: str, period: str) -> dict:
    try:
        return predict_asset(asset, timeframe, period)
    except Exception as e:
        return {"error": str(e)}


def main():
    if "theme" not in st.session_state:
        st.session_state.theme = "Dark"

    # Header Layout with Theme Toggle on the Right
    header_col, theme_col = st.columns([0.9, 0.1])
    
    with header_col:
        st.markdown('<div class="main-header">Trading Prophet ML 🚀</div>', unsafe_allow_html=True)
        
    with theme_col:
        st.write("") # Spacer
        # Button to toggle theme
        # If Dark, show Sun to switch to Light
        # If Light, show Moon to switch to Dark
        btn_label = "☀️" if st.session_state.theme == "Dark" else "🌙"
        
        if st.button(btn_label, key="theme_toggle"):
            st.session_state.theme = "Light" if st.session_state.theme == "Dark" else "Dark"
            st.rerun()
    
    is_dark = st.session_state.theme == "Dark"

    # Define Colors based on theme
    if is_dark:
        bg_color = "#0E1117"
        text_color = "#FAFAFA"
        card_bg = "#1E2130"
        metric_label = "#B0BEC5"
        metric_value_color = "#00E5FF" # Cyan for Dark Mode
        plotly_template = "plotly_dark"
    else:
        bg_color = "#FFFFFF"
        text_color = "#000000"       # Pure Black for max contrast
        card_bg = "#F0F2F6"          # Light Grey Card
        metric_label = "#333333"     # Dark Grey Label
        metric_value_color = "#0068C9" # Streamlit Blue for Light Mode (High Contrast)
        plotly_template = "plotly_white"

    # Inject Dynamic CSS
    st.markdown(f"""
    <style>
        /* Smooth fade-in animation */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .stApp {{
            background-color: {bg_color};
            color: {text_color};
            animation: fadeIn 0.5s ease-out;
        }}
        .main-header {{
            font-family: 'Helvetica Neue', sans-serif;
            font-weight: 700;
            font-size: 3rem;
            background: -webkit-linear-gradient(45deg, #00C9FF, #92FE9D);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-bottom: 2rem;
            animation: fadeIn 0.8s ease-out;
        }}
        .metric-card {{
            background-color: {card_bg};
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            text-align: center;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            transform-origin: center;
        }}
        .metric-card:hover {{
            transform: translateY(-5px) scale(1.02);
            box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
        }}
        .metric-value {{
            font-size: 2rem;
            font-weight: bold;
            color: {metric_value_color};
            transition: color 0.3s ease, transform 0.2s ease;
        }}
        .metric-card:hover .metric-value {{
            transform: scale(1.05);
        }}
        .metric-label {{
            font-size: 0.9rem;
            color: {metric_label};
            transition: color 0.3s ease;
        }}
        /* Smooth button transitions */
        .stButton > button {{
            transition: all 0.3s ease !important;
        }}
        .stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }}
        /* Smooth sidebar transitions */
        section[data-testid="stSidebar"] {{
            transition: all 0.3s ease;
        }}
        /* Smooth tab transitions */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
        }}
        .stTabs [data-baseweb="tab"] {{
            transition: all 0.3s ease;
        }}
        .stTabs [data-baseweb="tab"]:hover {{
            transform: translateY(-2px);
        }}
        /* Smooth plotly chart animation */
        .js-plotly-plot {{
            animation: fadeIn 0.6s ease-out;
        }}
        /* Smooth dataframe transitions */
        .stDataFrame {{
            animation: fadeIn 0.5s ease-out;
        }}
        /* Smooth info/warning/error boxes */
        .stAlert {{
            animation: fadeIn 0.4s ease-out;
            transition: all 0.3s ease;
        }}
        .stAlert:hover {{
            transform: translateX(5px);
        }}
        /* Hide Streamlit branding */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("### ⚙️ Asset Configuration")
    
    asset_type_raw = st.sidebar.radio("Asset Class", ["📈 Stocks", "🪙 Crypto", "💱 Forex", "🛠️ Custom"])
    asset_type = asset_type_raw.split(" ")[-1]
    
    if asset_type == "Stocks":
        region_options = list(STOCKS_BY_REGION.keys())
        region = st.sidebar.selectbox("Select Region/Country", region_options)
        
        # Simple stock selection without flags
        asset = st.sidebar.selectbox("Select Asset", STOCKS_BY_REGION[region], index=0)
        
    elif asset_type == "Crypto":
        asset = st.sidebar.selectbox("Select Pair", CRYPTO, index=0)
    elif asset_type == "Forex":
        display_name = st.sidebar.selectbox("Select Pair", list(FOREX_DISPLAY.keys()), index=0)
        asset = FOREX_DISPLAY[display_name]
    else:  # Custom
        asset_input = st.sidebar.text_input("Asset Symbol (yfinance/ccxt)", "NVDA")
        asset = asset_input.strip().upper()

    col1, col2 = st.sidebar.columns(2)
    with col1:
        timeframe = st.selectbox("Interval", ["1m", "5m", "15m", "1h", "4h", "1d", "1wk"], index=5)
    with col2:
        period = st.selectbox("Data Period", ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "max"], index=5)
    
    st.sidebar.markdown("### 🛠️ Chart Settings")
    show_volume = st.sidebar.checkbox("Show Volume", value=True)
    
    st.sidebar.markdown("**Overlays**")
    show_sma = st.sidebar.checkbox("SMA 20", value=True)
    show_ema = st.sidebar.checkbox("EMA 20", value=False)
    show_bb = st.sidebar.checkbox("Bollinger Bands", value=False)
    
    st.sidebar.markdown("**Oscillators**")
    show_rsi = st.sidebar.checkbox("RSI 14", value=False)
    show_macd = st.sidebar.checkbox("MACD", value=False)

    # Helper for custom metric cards
    def custom_metric(label, value, delta=None, color_trend=True):
        delta_html = ""
        if delta:
            # Parse delta to determine color
            delta_val = float(delta.strip('%').replace('+', ''))
            color = "#00FF00" if delta_val > 0 else "#FF0000"
            arrow = "↑" if delta_val > 0 else "↓"
            delta_html = f'<span style="color: {color}; font-size: 1rem; margin-left: 10px;">{arrow} {delta}</span>'
        
        return f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">
                {value}
                {delta_html}
            </div>
        </div>
        """

    if st.sidebar.button("Run Analysis", type="primary", use_container_width=True):
        with st.spinner(f"Fetching data and analyzing {asset}..."):
            analysis = cached_analysis(asset, timeframe, period)
            prediction = cached_prediction(asset, timeframe, period)

        if "error" in analysis:
            st.error(f"Analysis failed: {analysis['error']}")
            return
        
        if "error" in prediction:
            st.error(f"Prediction failed: {prediction['error']}")
            return

        # Main Dashboard Layout
        st.markdown(f"## {asset} Analysis & Forecast")
        
        # 1. Key Metrics Row
        if "history" in analysis:
            df = pd.DataFrame(analysis["history"])
            if not df.empty:
                last_close = df.iloc[-1]["close"]
                prev_close = df.iloc[-2]["close"]
                high_24h = df["high"].iloc[-24:].max() if len(df) >= 24 else df["high"].max()
                low_24h = df["low"].iloc[-24:].min() if len(df) >= 24 else df["low"].max()
                volume_24h = df["volume"].iloc[-24:].sum() if len(df) >= 24 else df["volume"].sum()
                
                change_pct = (last_close - prev_close) / prev_close * 100
                
                # Top Row: Signal & Price
                c1, c2, c3, c4 = st.columns(4)
                
                with c1:
                    st.markdown(custom_metric("Current Price", f"${last_close:,.2f}", f"{change_pct:+.2f}%"), unsafe_allow_html=True)
                
                with c2:
                    pred_price = prediction.get("prediction", 0)
                    pred_pct = (pred_price - last_close) / last_close * 100
                    st.markdown(custom_metric("Predicted Price", f"${pred_price:,.2f}", f"{pred_pct:+.2f}%"), unsafe_allow_html=True)
                
                with c3:
                    trend = "Bullish 🐂" if pred_pct > 0 else "Bearish 🐻"
                    st.markdown(custom_metric("Signal", trend), unsafe_allow_html=True)
                    
                with c4:
                     st.markdown(custom_metric("Confidence", f"{prediction.get('confidence', 0):.2f}"), unsafe_allow_html=True)

                # Calculate Date Range
                if 'timestamp' in df.columns:
                    dates = pd.to_datetime(df['timestamp'])
                else:
                    dates = pd.to_datetime(df.index)
                
                start_date = dates.min().strftime('%Y-%m-%d %H:%M')
                end_date = dates.max().strftime('%Y-%m-%d %H:%M')

                st.markdown(f"**Data Range:** `{start_date}` to `{end_date}`")

                # Second Row: Market Stats
                st.markdown(f"**Period Stats ({timeframe})**")
                s1, s2, s3, s4 = st.columns(4)
                s1.markdown(custom_metric("Highest (Last 24)", f"${high_24h:,.2f}"), unsafe_allow_html=True)
                s2.markdown(custom_metric("Lowest (Last 24)", f"${low_24h:,.2f}"), unsafe_allow_html=True)
                s3.markdown(custom_metric("Total Volume", f"{volume_24h:,.0f}"), unsafe_allow_html=True)
                s4.markdown(custom_metric("RSI (14)", f"{df.iloc[-1].get('rsi_14', 0):.2f}"), unsafe_allow_html=True)

        st.markdown("---")

        # 2. Tabs for Charts & Details
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Interactive Chart", "🧠 Analysis & Forecast", "📋 Raw Data", "📰 Latest News"])

        with tab1:
            if "history" in analysis and not df.empty:
                # Prepare X-axis data to ensure consistency across all traces
                x_data = df['timestamp'] if 'timestamp' in df.columns else df.index

                # Dynamic Subplots
                rows = 1
                row_heights = [0.7]
                
                if show_volume:
                    rows += 1
                    row_heights = [0.6, 0.15] if rows == 2 else [0.5, 0.15, 0.15]
                if show_rsi:
                    rows += 1
                    row_heights.append(0.15)
                if show_macd:
                    rows += 1
                    row_heights.append(0.15)
                
                # Normalize heights
                total = sum(row_heights)
                row_heights = [h/total for h in row_heights]

                subplot_titles = [f'{asset} Price ({start_date} - {end_date})']
                if show_volume: subplot_titles.append('Volume')
                if show_rsi: subplot_titles.append('RSI (14)')
                if show_macd: subplot_titles.append('MACD')

                fig = make_subplots(
                    rows=rows, cols=1, 
                    shared_xaxes=True, 
                    vertical_spacing=0.03, 
                    subplot_titles=subplot_titles, 
                    row_heights=row_heights
                )

                # 1. Candlestick (Main Chart) with smooth animations
                fig.add_trace(go.Candlestick(
                    x=x_data,
                    open=df['open'], high=df['high'], low=df['low'], close=df['close'],
                    name='OHLC',
                    increasing_line_color='#00FF88',
                    decreasing_line_color='#FF4444',
                    hoverinfo='x+y'
                ), row=1, col=1)

                # Overlays with smooth line rendering
                if show_sma and 'sma_20' in df.columns:
                    fig.add_trace(go.Scatter(
                        x=x_data, y=df['sma_20'], 
                        line=dict(color='orange', width=2, shape='spline'),
                        name='SMA 20',
                        mode='lines',
                        hovertemplate='<b>SMA 20</b><br>Price: $%{y:.2f}<extra></extra>'
                    ), row=1, col=1)
                if show_ema and 'ema_20' in df.columns:
                    fig.add_trace(go.Scatter(
                        x=x_data, y=df['ema_20'], 
                        line=dict(color='blue', width=2, shape='spline'),
                        name='EMA 20',
                        mode='lines',
                        hovertemplate='<b>EMA 20</b><br>Price: $%{y:.2f}<extra></extra>'
                    ), row=1, col=1)
                if show_bb and 'bb_upper' in df.columns:
                    fig.add_trace(go.Scatter(
                        x=x_data, y=df['bb_upper'], 
                        line=dict(color='rgba(150,150,150,0.5)', width=1, dash='dot', shape='spline'),
                        name='BB Upper',
                        mode='lines',
                        hovertemplate='<b>BB Upper</b><br>$%{y:.2f}<extra></extra>'
                    ), row=1, col=1)
                    fig.add_trace(go.Scatter(
                        x=x_data, y=df['bb_lower'], 
                        line=dict(color='rgba(150,150,150,0.5)', width=1, dash='dot', shape='spline'),
                        name='BB Lower', 
                        fill='tonexty',
                        fillcolor='rgba(150,150,150,0.1)',
                        mode='lines',
                        hovertemplate='<b>BB Lower</b><br>$%{y:.2f}<extra></extra>'
                    ), row=1, col=1)

                current_row = 2
                
                # 2. Volume with smooth bar animations
                if show_volume:
                    colors = ['#FF4444' if row['open'] - row['close'] >= 0 else '#00FF88' for index, row in df.iterrows()]
                    fig.add_trace(go.Bar(
                        x=x_data,
                        y=df['volume'], 
                        marker_color=colors,
                        marker_line_width=0,
                        opacity=0.7,
                        showlegend=False, 
                        name='Volume',
                        hovertemplate='<b>Volume</b><br>%{y:,.0f}<extra></extra>'
                    ), row=current_row, col=1)
                    current_row += 1

                # 3. RSI with smooth curves
                if show_rsi and 'rsi_14' in df.columns:
                    fig.add_trace(go.Scatter(
                        x=x_data, y=df['rsi_14'], 
                        line=dict(color='#B794F4', width=2, shape='spline'),
                        name='RSI',
                        mode='lines',
                        fill='tozeroy',
                        fillcolor='rgba(183, 148, 244, 0.1)',
                        hovertemplate='<b>RSI</b><br>%{y:.2f}<extra></extra>'
                    ), row=current_row, col=1)
                    fig.add_hline(y=70, line_dash="dash", line_color="rgba(255,100,100,0.5)", line_width=1, row=current_row, col=1)
                    fig.add_hline(y=30, line_dash="dash", line_color="rgba(100,255,100,0.5)", line_width=1, row=current_row, col=1)
                    current_row += 1

                # 4. MACD with smooth animations
                if show_macd and 'macd' in df.columns:
                    fig.add_trace(go.Scatter(
                        x=x_data, y=df['macd'], 
                        line=dict(color='#4299E1', width=2, shape='spline'),
                        name='MACD',
                        mode='lines',
                        hovertemplate='<b>MACD</b><br>%{y:.4f}<extra></extra>'
                    ), row=current_row, col=1)
                    fig.add_trace(go.Scatter(
                        x=x_data, y=df['macd_signal'], 
                        line=dict(color='#ED8936', width=2, shape='spline'),
                        name='Signal',
                        mode='lines',
                        hovertemplate='<b>Signal</b><br>%{y:.4f}<extra></extra>'
                    ), row=current_row, col=1)
                    # Histogram bars with color coding
                    hist_colors = ['#00FF88' if val >= 0 else '#FF4444' for val in df['macd_hist']]
                    fig.add_trace(go.Bar(
                        x=x_data, y=df['macd_hist'],
                        name='Hist',
                        marker_color=hist_colors,
                        marker_line_width=0,
                        opacity=0.6,
                        hovertemplate='<b>Histogram</b><br>%{y:.4f}<extra></extra>'
                    ), row=current_row, col=1)
                    current_row += 1

                # Update layout with smooth animations and transitions
                fig.update_layout(
                    height=800 if rows > 2 else 600,
                    xaxis_rangeslider_visible=True,
                    xaxis_rangeslider_thickness=0.05,
                    template=plotly_template,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=20, r=20, t=40, b=20),
                    legend=dict(
                        orientation="h", 
                        yanchor="bottom", 
                        y=1.02, 
                        xanchor="right", 
                        x=1,
                        bgcolor='rgba(0,0,0,0.5)',
                        bordercolor='rgba(255,255,255,0.2)',
                        borderwidth=1
                    ),
                    # Smooth animations and transitions
                    transition={
                        'duration': 500,
                        'easing': 'cubic-in-out'
                    },
                    hovermode='x unified',
                    hoverlabel=dict(
                        bgcolor='rgba(0,0,0,0.8)',
                        font_size=13,
                        font_family="Arial",
                        font_color="white",
                        bordercolor='rgba(255,255,255,0.3)'
                    ),
                    # Smooth drag and zoom
                    dragmode='zoom',
                )
                
                # Add smooth animations to all traces
                fig.update_traces(
                    hoverinfo='all',
                    hoverlabel=dict(namelength=-1)
                )
                
                # Smooth axis transitions
                fig.update_xaxes(
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='rgba(128,128,128,0.1)',
                    showline=True,
                    linewidth=1,
                    linecolor='rgba(128,128,128,0.3)',
                )
                
                fig.update_yaxes(
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='rgba(128,128,128,0.1)',
                    showline=True,
                    linewidth=1,
                    linecolor='rgba(128,128,128,0.3)',
                )
                
                # Display with animation configuration
                st.plotly_chart(
                    fig, 
                    use_container_width=True,
                    config={
                        'displayModeBar': True,
                        'displaylogo': False,
                        'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
                        'toImageButtonOptions': {
                            'format': 'png',
                            'filename': f'{asset}_chart',
                            'height': 1080,
                            'width': 1920,
                            'scale': 2
                        }
                    }
                )
            else:
                st.warning("No historical data available for plotting.")

        with tab2:
            st.markdown(f"### AI Prediction & Analysis: {asset}")

            latest_data_ts = prediction.get("data_last_updated") or analysis.get("data_last_updated")
            if latest_data_ts:
                st.caption(f"Latest market data timestamp (UTC): {latest_data_ts}")
            
            # 1. Main Findings / Narrative
            if "findings" in prediction:
                st.info(f"**Key Insight:** {prediction['findings']}")
            
            st.markdown("---")

            # 2. Strategy Performance (Backtest)
            st.markdown("#### 📊 Strategy Performance (Backtest)")
            st.caption("How this strategy would have performed on historical data.")
            
            metrics = analysis.get("metrics", {})
            if metrics:
                m1, m2, m3, m4 = st.columns(4)
                
                with m1:
                    val = metrics.get('total_return', 0)
                    st.metric("Total Return", f"{val*100:.2f}%", help="The total percentage profit or loss generated by the strategy over the selected period.")
                with m2:
                    val = metrics.get('annualized_return', 0)
                    st.metric("Annualized Return", f"{val*100:.2f}%", help="The theoretical yearly return if this performance were sustained for a full year.")
                with m3:
                    sharpe = metrics.get('sharpe_ratio', 0)
                    st.metric("Sharpe Ratio", f"{sharpe:.2f}", help="A measure of risk-adjusted return. > 1.0 is generally considered 'good'. Higher is better.")
                with m4:
                    dd = metrics.get('max_drawdown', 0)
                    st.metric("Max Drawdown", f"{dd*100:.2f}%", help="The largest single drop from a peak to a trough. Represents the worst-case loss during the period.")
            else:
                st.write("No backtest metrics available.")

            st.markdown("---")

            # 3. Model Details & Explanation
            c1, c2 = st.columns([0.5, 0.5])
            
            with c1:
                st.markdown("#### 🧠 Prediction Confidence")
                conf = prediction.get('confidence', 0)
                st.markdown(f"**Level:** `{conf:.2f}`")
                
                if conf > 0.7:
                    st.success("✅ **High Confidence**: The model sees strong, clear patterns. The prediction is more likely to be accurate.")
                elif conf > 0.4:
                    st.warning("⚠️ **Moderate Confidence**: Some patterns are present, but the market is slightly noisy.")
                else:
                    st.error("🛑 **Low Confidence**: The market is very unpredictable right now. Treat this signal with extra caution.")

            with c2:
                st.markdown("#### ℹ️ What does this mean?")
                st.markdown("""
                - **Bullish 🐂**: The AI predicts prices will **rise**.
                - **Bearish 🐻**: The AI predicts prices will **fall**.
                - **Horizon**: The prediction is for the *next few periods* (e.g., next 5 days if using Daily interval).
                """)

            with st.expander("📚 Guide: How to read these numbers (Click to Expand)"):
                st.markdown("""
                **1. Total Return**  
                The overall profit or loss. If you started with $100 and this says 10%, you'd have $110.
                
                **2. Sharpe Ratio (Risk vs Reward)**  
                Think of this as "Bang for your Buck".  
                - **> 1.0**: Great! Useable strategy.  
                - **< 1.0**: Be careful. The returns might not be worth the roller-coaster ride.
                
                **3. Max Drawdown (The "Pain" Index)**  
                This is the worst loss you would have seen in your account at any single point.  
                - Example: If you bought at the very top and the price crashed 20% before recovering, the Max Drawdown is 20%. **Lower is better.**
                """)            
                
            st.caption(f"Disclaimer: {prediction.get('disclaimer', 'Not financial advice.')}")

        with tab3:
            st.dataframe(df if "history" in analysis else pd.DataFrame())

        with tab4:
            news_items = analysis.get("latest_news") or prediction.get("latest_news") or []
            if news_items:
                st.caption("Latest headlines are pulled at analysis time from live feeds.")
                for item in news_items:
                    title = item.get("title", "Untitled")
                    source = item.get("source", "Unknown source")
                    published_at = item.get("published_at", "")
                    url = item.get("url", "")
                    st.markdown(f"- **{source}** ({published_at})  ")
                    if url:
                        st.markdown(f"  [{title}]({url})")
                    else:
                        st.write(f"  {title}")
            else:
                st.info("No recent news found for this asset right now.")

    else:
        # Placeholder or Landing Page
        st.info("👈 Select an asset from the sidebar and click **Run Analysis** to start.")
        st.markdown("### 🌎 Global Asset Coverage")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Stocks")
            examples = []
            for r, s_list in list(STOCKS_BY_REGION.items())[:5]:
                examples.append(f"{r}: {s_list[0]}")
            st.write(", ".join(examples) + " ...")
            
        with c2:
            st.markdown("#### 🪙 Cryptocurrencies")
            st.write(", ".join([f"🪙 {c}" for c in CRYPTO[:5]]) + " ...")
            
        st.markdown("#### 💱 Forex Pairs")
        st.write(", ".join(list(FOREX_DISPLAY.keys())[:5]) + " ...")

if __name__ == "__main__":
    main()
