"""
Trading Journal Page
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

from utils.journal import (
    load_journal,
    compute_stats,
    clear_journal,
    log_trades,
    preview_trade_import,
)
from core.config import Config
from utils.theme import apply_app_theme

st.set_page_config(
    page_title="Journal - Swing Trader",
    page_icon="📓",
    layout="wide"
)

apply_app_theme()

st.markdown(
    """
    <div class="hero-panel">
        <div class="status-pill">PERFORMANCE TRACKER &nbsp;•&nbsp; TRADE JOURNAL</div>
        <h1 style="margin:0;font-size:1.75rem;font-weight:800;letter-spacing:-0.025em;">📓 Trading Journal</h1>
        <p style="margin:0.5rem 0 0 0;font-size:0.95rem;color:var(--text-secondary);">Lacak setiap trade, analisis equity curve, dan evaluasi performa strategi secara objektif.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Load journal data
journal_df = load_journal()
stats = compute_stats()

# Sidebar
st.sidebar.header("⚙️ Journal Actions")

if st.sidebar.button("🔄 Refresh Data", use_container_width=True):
    st.cache_data.clear()
    st.rerun()

if st.sidebar.button("🗑️ Clear Journal", type="secondary", use_container_width=True):
    if st.sidebar.checkbox("Yakin ingin menghapus semua data?"):
        if clear_journal():
            st.sidebar.success("✅ Journal cleared!")
            st.rerun()
        else:
            st.sidebar.error("❌ Gagal menghapus journal")

# Main content
if journal_df.empty:
    st.info("📭 Journal masih kosong. Mulai trading atau import data backtest!")
    
    st.markdown("""
    ### Cara Mengisi Journal:
    
    1. **Otomatis dari Backtest**: Hasil backtest otomatis tersimpan di journal
    2. **Manual Import**: Upload CSV dengan format yang sesuai
    3. **Real Trading**: Catat trade Anda secara manual
    
    Format CSV yang diperlukan:
    - entry_time, exit_time, entry, exit, size, sl, tp, reason, pnl, r_multiple, equity_after
    """)
    
    # File uploader for manual import
    uploaded_file = st.file_uploader("Upload CSV Journal", type=['csv'])
    if uploaded_file is not None:
        try:
            df_upload = pd.read_csv(uploaded_file)
            is_valid, message, preview_stats = preview_trade_import(df_upload)
            if not is_valid:
                st.error(f"❌ Format CSV tidak valid: {message}")
                st.stop()

            st.success("✅ Format CSV valid")

            col_a, col_b, col_c, col_d = st.columns(4)
            with col_a:
                st.metric("Total Rows", preview_stats["total_rows"])
            with col_b:
                st.metric("Rows Baru", preview_stats["new_rows"])
            with col_c:
                st.metric("Duplikat di File", preview_stats["duplicate_in_file"])
            with col_d:
                st.metric("Sudah Ada di Journal", preview_stats["duplicate_in_journal"])

            with st.expander("Preview Data Import"):
                st.dataframe(df_upload.head(20), use_container_width=True, hide_index=True)

            if preview_stats["new_rows"] == 0:
                st.info("ℹ️ Tidak ada baris baru untuk diimport (semua duplikat).")
            elif st.button("📥 Konfirmasi Import ke Journal", type="primary", use_container_width=True):
                if log_trades(df_upload):
                    st.success("✅ Data berhasil diimport!")
                    st.rerun()
                else:
                    st.error("❌ Gagal menyimpan data ke journal")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    
    st.stop()

# Statistics Section
st.markdown('<p class="section-label" style="margin-top:0.5rem;">Overall Performance</p>', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total Trades", stats["total_trades"])

with col2:
    win_rate_color = "normal" if stats["win_rate"] >= 50 else "inverse"
    st.metric("Win Rate", f"{stats['win_rate']}%")

with col3:
    st.metric("Avg R-Multiple", f"{stats['avg_r_multiple']}R")

with col4:
    pnl = stats["total_pnl"]
    pnl_color = "normal" if pnl >= 0 else "inverse"
    st.metric("Total PnL", f"Rp {pnl:,.0f}")

with col5:
    st.metric("Win/Loss", f"{stats['winning_trades']}/{stats['losing_trades']}")

# Equity Curve
st.markdown('<p class="section-label" style="margin-top:1rem;">Equity Curve</p>', unsafe_allow_html=True)

if "equity_after" in journal_df.columns:
    fig_equity = go.Figure()
    
    fig_equity.add_trace(go.Scatter(
        x=journal_df.index,
        y=journal_df["equity_after"],
        mode='lines+markers',
        name='Equity',
        line=dict(color='#3B82F6', width=2.5),
        marker=dict(size=5, color='#60A5FA'),
        fill='tozeroy',
        fillcolor='rgba(59,130,246,0.08)'
    ))
    
    fig_equity.update_layout(
        title=dict(text="Equity Curve", font=dict(size=14, color='#F8FAFC')),
        xaxis_title="Trade #",
        yaxis_title="Equity (Rp)",
        hovermode='x unified',
        height=380,
        paper_bgcolor='rgba(17,24,39,0.5)',
        plot_bgcolor='rgba(17,24,39,0.5)',
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)', color='#94A3B8'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)', color='#94A3B8'),
        font=dict(color='#94A3B8', family='Plus Jakarta Sans, sans-serif'),
        margin=dict(l=10, r=10, t=40, b=10),
    )
    
    st.plotly_chart(fig_equity, use_container_width=True)

# Performance Analysis
st.markdown('<p class="section-label" style="margin-top:1rem;">Performance Analysis</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # R-Multiple Distribution
    if "r_multiple" in journal_df.columns:
        fig_r = px.histogram(
            journal_df,
            x="r_multiple",
            nbins=30,
            title="R-Multiple Distribution",
            labels={"r_multiple": "R-Multiple", "count": "Frequency"},
            color_discrete_sequence=["#3B82F6"],
        )
        fig_r.add_vline(x=0, line_dash="dash", line_color="#EF4444", line_width=1.5)
        fig_r.update_layout(
            height=350,
            paper_bgcolor='rgba(17,24,39,0.5)', plot_bgcolor='rgba(17,24,39,0.5)',
            xaxis=dict(gridcolor='rgba(255,255,255,0.05)', color='#94A3B8'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.05)', color='#94A3B8'),
            font=dict(color='#94A3B8', family='Plus Jakarta Sans, sans-serif'),
            title=dict(font=dict(color='#F8FAFC', size=13)),
            margin=dict(l=10, r=10, t=40, b=10),
        )
        st.plotly_chart(fig_r, use_container_width=True)

with col2:
    # Win/Loss Pie Chart
    if stats["total_trades"] > 0:
        fig_pie = go.Figure()
        fig_pie.add_trace(go.Pie(
            labels=['Winning Trades', 'Losing Trades'],
            values=[stats["winning_trades"], stats["losing_trades"]],
            marker_colors=['#10B981', '#EF4444'],
            hole=0.5,
            textfont=dict(color='#F8FAFC'),
        ))
        fig_pie.update_layout(
            title=dict(text="Win/Loss Ratio", font=dict(color='#F8FAFC', size=13)),
            height=350,
            paper_bgcolor='rgba(17,24,39,0.5)',
            font=dict(color='#94A3B8', family='Plus Jakarta Sans, sans-serif'),
            legend=dict(font=dict(color='#94A3B8')),
            margin=dict(l=10, r=10, t=40, b=10),
        )
        st.plotly_chart(fig_pie, use_container_width=True)

# PnL Over Time
if "pnl" in journal_df.columns:
    st.markdown('<p class="section-label" style="margin-top:1rem;">PnL Per Trade</p>', unsafe_allow_html=True)
    
    fig_pnl = go.Figure()
    
    colors = ['#10B981' if x > 0 else '#EF4444' for x in journal_df["pnl"]]
    
    fig_pnl.add_trace(go.Bar(
        x=journal_df.index,
        y=journal_df["pnl"],
        marker_color=colors,
        marker_line_width=0,
        name='PnL'
    ))
    
    fig_pnl.add_hline(y=0, line_dash="dash", line_color="rgba(255,255,255,0.2)", line_width=1)
    
    fig_pnl.update_layout(
        title=dict(text="Profit / Loss per Trade", font=dict(color='#F8FAFC', size=13)),
        xaxis_title="Trade #",
        yaxis_title="PnL (Rp)",
        height=380,
        paper_bgcolor='rgba(17,24,39,0.5)', plot_bgcolor='rgba(17,24,39,0.5)',
        xaxis=dict(gridcolor='rgba(255,255,255,0.04)', color='#94A3B8'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.04)', color='#94A3B8'),
        font=dict(color='#94A3B8', family='Plus Jakarta Sans, sans-serif'),
        margin=dict(l=10, r=10, t=40, b=10),
    )
    
    st.plotly_chart(fig_pnl, use_container_width=True)

# Trade Details Table
st.markdown('<p class="section-label" style="margin-top:1rem;">Trade Log</p>', unsafe_allow_html=True)

# Filter options
col1, col2, col3 = st.columns(3)

with col1:
    filter_result = st.selectbox(
        "Filter by Result",
        ["All", "Winning", "Losing"],
        index=0
    )

with col2:
    if "reason" in journal_df.columns:
        reasons = ["All"] + list(journal_df["reason"].unique())
        filter_reason = st.selectbox(
            "Filter by Exit Reason",
            reasons,
            index=0
        )
    else:
        filter_reason = "All"

with col3:
    sort_by = st.selectbox(
        "Sort by",
        ["Entry Time", "PnL", "R-Multiple"],
        index=0
    )

# Apply filters
df_filtered = journal_df.copy()

if filter_result == "Winning":
    df_filtered = df_filtered[df_filtered["pnl"] > 0]
elif filter_result == "Losing":
    df_filtered = df_filtered[df_filtered["pnl"] <= 0]

if filter_reason != "All" and "reason" in df_filtered.columns:
    df_filtered = df_filtered[df_filtered["reason"] == filter_reason]

# Sort
if sort_by == "Entry Time" and "entry_time" in df_filtered.columns:
    df_filtered = df_filtered.sort_values("entry_time", ascending=False)
elif sort_by == "PnL" and "pnl" in df_filtered.columns:
    df_filtered = df_filtered.sort_values("pnl", ascending=False)
elif sort_by == "R-Multiple" and "r_multiple" in df_filtered.columns:
    df_filtered = df_filtered.sort_values("r_multiple", ascending=False)

# Display table
if not df_filtered.empty:
    # Format for display
    df_display = df_filtered.copy()
    
    # Format dates if present
    if "entry_time" in df_display.columns:
        df_display["entry_time"] = pd.to_datetime(df_display["entry_time"]).dt.strftime("%Y-%m-%d")
    if "exit_time" in df_display.columns:
        df_display["exit_time"] = pd.to_datetime(df_display["exit_time"]).dt.strftime("%Y-%m-%d")
    
    # Color code based on profit/loss
    def highlight_pnl(row):
        if "pnl" in row and row["pnl"] > 0:
            return ['background-color: #d4edda'] * len(row)
        else:
            return ['background-color: #f8d7da'] * len(row)
    
    st.dataframe(
        df_display.style.apply(highlight_pnl, axis=1),
        use_container_width=True,
        hide_index=True
    )
    
    # Summary of filtered data
    st.markdown("#### Filtered Statistics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Trades Shown", len(df_filtered))
    with col2:
        if "pnl" in df_filtered.columns:
            total_pnl = df_filtered["pnl"].sum()
            st.metric("Total PnL", f"Rp {total_pnl:,.0f}")
    with col3:
        if "r_multiple" in df_filtered.columns:
            avg_r = df_filtered["r_multiple"].mean()
            st.metric("Avg R", f"{avg_r:.2f}R")
    
else:
    st.info("No trades match the selected filters.")

# Download section
st.markdown("---")
col1, col2 = st.columns([3, 1])

with col2:
    csv = journal_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Full Journal",
        data=csv,
        file_name=f"trading_journal_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        use_container_width=True
    )

# Info section
with st.expander("ℹ️ Tentang Journal"):
    st.markdown("""
    ### Trading Journal
    
    Journal ini mencatat semua trade Anda untuk analisis performa. Data bisa berasal dari:
    
    - **Backtest**: Otomatis tersimpan saat menjalankan backtest
    - **Real Trading**: Import CSV dari broker atau catat manual
    - **Simulasi**: Import hasil simulasi trading
    
    ### Metrik Penting:
    
    - **Win Rate**: Persentase trade yang profit
    - **Avg R-Multiple**: Rata-rata profit dalam kelipatan risiko
    - **Total PnL**: Total profit/loss keseluruhan
    - **Equity Curve**: Pertumbuhan modal over time
    
    ### Tips:
    
    - Review journal secara rutin
    - Identifikasi pola kemenangan dan kekalahan
    - Fokus pada konsistensi, bukan trade individual
    - Target: Win Rate > 50%, Avg R > 1
    """)
