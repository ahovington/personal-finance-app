import os

import streamlit as st

from page_actuals import actuals
from page_budget import budget
from src_mockdata import BudgetDataMock
from src_upbank import BudgetDataUp, UpbankClient

DATABASE_CONNECTION = "./db/db.duckdb"
UPBANK_TOKEN = os.getenv("UPBANK_TOKEN")
IS_MOCK_DATA = os.getenv("IS_MOCK_DATA", False)
REFRESH_DATA = os.getenv("REFRESH_DATA", False)  # THIS Needs to be a button somewhere.

if IS_MOCK_DATA:
    generator = BudgetDataMock()
else:
    client = UpbankClient(UPBANK_TOKEN)
    generator = BudgetDataUp(client, DATABASE_CONNECTION)

st.set_page_config(
    page_title="Budget Application",
    page_icon="💵",
    layout="wide",
    initial_sidebar_state="auto",
)

pages = {"Actuals": actuals, "Budget": budget}
page = st.sidebar.selectbox("PAGES", ["Actuals", "Budget"])
pages[page](generator)
