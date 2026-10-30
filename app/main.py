"""Entry point for the virtual portfolio Streamlit application."""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.theme import setup_page, workspace_card  # noqa: E402
from src.db import database_ready  # noqa: E402

setup_page("Home")
st.title("Portfolio Lab")
st.caption("A focused workspace for exploring an NSE virtual portfolio.")

intro, overview = st.columns([1.45, 1], vertical_alignment="center")
with intro:
    st.subheader("Make every practice trade legible")
    st.write("Track a virtual portfolio, test technical signals, understand risk, and inspect the price history behind every view.")
with overview:
    st.info("**Explore the workspace**\n\nDashboard for positions · Trade for virtual orders · Risk and Signals for analysis.")

st.markdown("### Explore the workspace")
first_row = st.columns(2)
with first_row[0]:
    workspace_card("Dashboard", "Review portfolio value, holdings, allocation, and market movers.",
                   "pages/1_Dashboard.py", icon="↗", action="Open dashboard")
with first_row[1]:
    workspace_card("Virtual trading", "Place simulated buy and sell orders using the latest stored close.",
                   "pages/2_Trade.py", icon="↔", action="Place an order")
second_row = st.columns(2)
with second_row[0]:
    workspace_card("Risk analysis", "Explore drawdown, correlation, volatility, and historical VaR.",
                   "pages/3_Risk.py", icon="◒", action="View risk analysis")
with second_row[1]:
    workspace_card("Signals & backtesting", "Compare rule-based signals against buy-and-hold performance.",
                   "pages/4_Signals.py", icon="⌁", action="Explore signals")

if database_ready():
    st.success("Market data and the ₹10,00,000 demo portfolio are ready. Choose a page in the sidebar.")
else:
    st.error("The database is not ready. Run `python -m src.data_pipeline` first.")
