"""Shared finance dashboard colours, formatting and page chrome."""

from __future__ import annotations

import math
import sys

from pathlib import Path

_LOCAL_DEPS = Path(__file__).resolve().parents[1] / ".deps"
if _LOCAL_DEPS.exists() and str(_LOCAL_DEPS) not in sys.path:
    sys.path.append(str(_LOCAL_DEPS))

import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st

from src.config import DISCLAIMER

# A calm, paper-like research terminal palette. Keep these semantic names because
# every chart and page consumes them through this one module.
BG = "#F4F7FB"
SURFACE = "#FFFFFF"
BORDER = "#D9E2EF"
TEXT = "#14213D"
MUTED = "#64748B"
TEAL = "#0F766E"
INDIGO = "#3157C8"
AMBER = "#B7791F"
PROFIT = "#15803D"
LOSS = "#C2413B"

TEMPLATE = go.layout.Template(
    layout=go.Layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Manrope, Inter, sans-serif", "color": TEXT},
        colorway=[TEAL, INDIGO, AMBER, PROFIT, LOSS, MUTED],
        xaxis={"gridcolor": "#E9EFF7", "zerolinecolor": BORDER, "linecolor": BORDER},
        yaxis={"gridcolor": "#E9EFF7", "zerolinecolor": BORDER, "linecolor": BORDER},
        legend={"bgcolor": "rgba(0,0,0,0)"},
    )
)
pio.templates["portfolio_dark"] = TEMPLATE


def chart_layout(fig: go.Figure, *, height: int = 390) -> go.Figure:
    """Apply the one reusable chart template and common spacing."""
    fig.update_layout(
        template="portfolio_dark",
        height=height,
        margin=dict(l=12, r=18, t=64, b=28),
        hovermode="x unified",
        autosize=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    )
    fig.update_xaxes(automargin=True)
    fig.update_yaxes(automargin=True)
    return fig


def indian_number(value: float) -> str:
    """Format a number with Indian digit grouping and two decimals."""
    if not math.isfinite(value):
        return "—"
    sign = "-" if value < 0 else ""
    whole, decimals = f"{abs(value):.2f}".split(".")
    if len(whole) > 3:
        head, tail = whole[:-3], whole[-3:]
        chunks = []
        while head:
            chunks.append(head[-2:])
            head = head[:-2]
        whole = ",".join(reversed(chunks)) + "," + tail
    return f"{sign}{whole}.{decimals}"


def inr(value: float) -> str:
    """Format money in Indian rupees."""
    formatted = indian_number(value)
    return "—" if formatted == "—" else f"₹{formatted}"


def signed_inr(value: float) -> str:
    """Show P&L direction with an arrow in addition to any colour."""
    return f"{'▲' if value >= 0 else '▼'} {inr(abs(value))}"


def percent(value: float, *, arrow: bool = False) -> str:
    """Format a ratio as a two-decimal percentage."""
    if value is None or not math.isfinite(value):
        return "—"
    prefix = ("▲ " if value >= 0 else "▼ ") if arrow else ""
    return f"{prefix}{abs(value) * 100:.2f}%" if arrow else f"{value * 100:.2f}%"


def render_sidebar() -> None:
    """Render the one compact navigation system used by every Streamlit page."""
    with st.sidebar:
        with st.container(border=True):
            st.markdown("""
                <div class="brand-lockup">
                    <div class="brand-mark">PL</div>
                    <div><div class="brand-name">Portfolio Lab</div><div class="brand-subtitle">Virtual NSE workspace</div></div>
                </div>
                <div class="nav-kicker">Workspace</div>
            """, unsafe_allow_html=True)
            st.page_link("main.py", label="Overview", icon=":material/home:")
            st.page_link("pages/1_Dashboard.py", label="Dashboard", icon=":material/dashboard:")
            st.page_link("pages/2_Trade.py", label="Virtual Trading", icon=":material/swap_horiz:")
            st.page_link("pages/3_Risk.py", label="Risk Analysis", icon=":material/shield:")
            st.page_link("pages/4_Signals.py", label="Signals & Backtesting", icon=":material/query_stats:")
            st.page_link("pages/5_Data_Explorer.py", label="Data Explorer", icon=":material/table_chart:")


def workspace_card(title: str, description: str, page: str, *, icon: str, action: str) -> None:
    """Render a compact, functional landing-page link card."""
    with st.container(border=True):
        st.markdown(f"<div class='workspace-icon'>{icon}</div>", unsafe_allow_html=True)
        st.markdown(f"#### {title}")
        st.caption(description)
        st.page_link(page, label=action)


def setup_page(title: str) -> None:
    """Set shared metadata, visual chrome, responsive grid, and navigation."""
    st.set_page_config(page_title=f"{title} | Portfolio Lab", page_icon="📈", layout="wide")
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');
        :root { --page-bg: #F4F7FB; --surface: #FFFFFF; --ink: #14213D; --muted: #64748B; --line: #D9E2EF; --nav: #14213D; --nav-hover: #20345A; --primary: #3157C8; }
        html, body, [class*="css"], [data-testid="stApp"] { font-family: Manrope, system-ui, sans-serif; }
        [data-testid="stApp"] { background: #F4F7FB; color: #14213D; }
        [data-testid="stSidebar"], [data-testid="stSidebar"] > div:first-child { background: #14213D; }
        [data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"] { background: #FFFFFF; border: 1px solid #E8EDF5; border-radius: 14px; box-shadow: none; padding: 16px; }
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
        [data-testid="stSidebar"] label, [data-testid="stSidebar"] p { color: #172B4D; }
        [data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] { align-items: center; border-radius: 8px; color: #263653; display: flex; font-size: .91rem; font-weight: 600; gap: 12px; min-height: 43px; margin: 0 0 8px; padding: 10px 12px; position: relative; transition: background-color 140ms ease, color 140ms ease; }
        [data-testid="stSidebar"] [data-testid="stPageLink-NavLink"]:hover { background: #F3F6FB; color: #172B4D; }
        [data-testid="stSidebar"] [data-testid="stPageLink-NavLink"][aria-current="page"] { background: #EAF1FF; color: #244FA8; font-weight: 700; }
        [data-testid="stSidebar"] [data-testid="stPageLink-NavLink"][aria-current="page"]::before { background: #315ECA; border-radius: 0 2px 2px 0; content: ""; height: 22px; left: 0; position: absolute; top: 10px; width: 3px; }
        [data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] [data-testid="stIconMaterial"],
        [data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] .material-symbols-rounded { color: #64748B; flex: 0 0 20px; font-size: 20px; height: 20px; line-height: 20px; width: 20px; }
        [data-testid="stSidebar"] [data-testid="stPageLink-NavLink"][aria-current="page"] [data-testid="stIconMaterial"],
        [data-testid="stSidebar"] [data-testid="stPageLink-NavLink"][aria-current="page"] .material-symbols-rounded { color: #315ECA; }
        .brand-lockup { align-items: center; border-bottom: 1px solid #E8EDF5; display: flex; gap: 10px; margin-bottom: 18px; padding: 2px 2px 16px; }
        .brand-mark { align-items: center; background: #EAF1FF; border-radius: 8px; color: #315ECA; display: flex; font-family: "DM Mono", monospace; font-size: .72rem; font-weight: 500; height: 34px; justify-content: center; width: 34px; }
        .brand-name { color: #172B4D; font-size: 1rem; font-weight: 800; letter-spacing: -.02em; line-height: 1.2; }
        .brand-subtitle { color: #64748B; font-size: .71rem; margin-top: 2px; }
        .nav-kicker { color: #64748B; font-size: .68rem; font-weight: 800; letter-spacing: .1em; margin: 0 0 10px 2px; text-transform: uppercase; }
        [data-testid="stHeader"] { background: rgba(244,247,251,.94); border-bottom: 1px solid #D9E2EF; height: 3.5rem; }
        h1, h2, h3 { color: #14213D; letter-spacing: -.035em; }
        h1 { font-size: clamp(1.75rem, 2.5vw, 2.35rem); font-weight: 800 !important; line-height: 1.18; margin-bottom: .2rem !important; }
        h2, h3 { font-weight: 700 !important; }
        [data-testid="stMetric"] { background: #FFFFFF; border: 1px solid #D9E2EF;
          border-radius: 14px; padding: 17px 20px; box-shadow: 0 5px 16px rgba(20,33,61,.055); }
        [data-testid="stMetricLabel"] { color: #64748B; font-size: .8rem; font-weight: 700; letter-spacing: .035em; text-transform: uppercase; }
        [data-testid="stMetricValue"] { color: #14213D; font-family: "DM Mono", monospace; font-size: 1.45rem; }
        [data-testid="stMetricValue"], [data-testid="stMetricDelta"] { font-variant-numeric: tabular-nums; }
        [data-testid="stDataFrame"] { border: 1px solid #D9E2EF; border-radius: 10px; overflow: hidden; }
        [data-testid="stExpander"] { background: #FFFFFF; border: 1px solid #D9E2EF; border-radius: 12px; }
        [data-testid="stVerticalBlockBorderWrapper"] { background: #FFFFFF; border-color: #D9E2EF; border-radius: 12px; box-shadow: 0 4px 14px rgba(20,33,61,.035); }
        .workspace-icon { align-items: center; background: #E9F2FF; border-radius: 8px; color: #3157C8; display: flex; font-size: 1rem; height: 34px; justify-content: center; margin-bottom: 14px; width: 34px; }
        [data-testid="stVerticalBlockBorderWrapper"] h4 { font-size: 1rem; margin: 0 0 .3rem; }
        [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stPageLink-NavLink"] { color: #3157C8; font-size: .86rem; font-weight: 700; margin-top: .3rem; padding: 4px 0; }
        .stButton button, .stDownloadButton button { border-radius: 9px; font-weight: 700; border-color: #B7C6DA; }
        .stButton button[kind="primary"] { background: #3157C8; border-color: #3157C8; }
        .stButton button[kind="primary"]:hover { background: #2748AA; border-color: #2748AA; }
        [data-baseweb="select"] > div, [data-baseweb="input"] > div { border-radius: 9px; border-color: #C7D3E3; }
        .simulation-banner { background: #E9F2FF; border: 1px solid #BBD5F7;
          border-radius: 10px; padding: 10px 14px; color: #23417B; margin-bottom: 20px; font-size: .86rem; }
        .simulation-footer { position: fixed; bottom: 0; left: 0; right: 0; z-index: 999;
          background: #FFFFFF; border-top: 1px solid #D9E2EF; color: #64748B;
          text-align: center; padding: 7px 12px; font-size: 12px; }
        .main .block-container { max-width: 1240px; padding: 1.35rem 2rem 5rem; }
        [data-testid="stHorizontalBlock"] { gap: 1rem; }
        [data-testid="stCaptionContainer"] { color: #64748B; }
        @media (min-width: 769px) {
          [data-testid="stSidebar"][aria-expanded="true"], [data-testid="stSidebar"][aria-expanded="true"] > div:first-child { min-width: 260px !important; width: 260px !important; }
        }
        @media (max-width: 768px) {
          .main .block-container { padding: 1rem 1rem 4.5rem; }
          [data-testid="stSidebar"][aria-expanded="true"], [data-testid="stSidebar"][aria-expanded="true"] > div:first-child { min-width: min(86vw, 300px) !important; width: min(86vw, 300px) !important; }
          [data-testid="stHorizontalBlock"] { gap: .75rem; }
        }
        @media (max-width: 640px) {
          [data-testid="stHorizontalBlock"] > [data-testid="column"] { flex: 1 1 100% !important; min-width: 100% !important; width: 100% !important; }
          [data-testid="stMetric"] { padding: 14px 16px; }
          .simulation-banner { margin-bottom: 16px; }
        }
        </style>
    """, unsafe_allow_html=True)
    render_sidebar()
    st.markdown(f'<div class="simulation-banner">{DISCLAIMER}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="simulation-footer">{DISCLAIMER}</div>', unsafe_allow_html=True)
