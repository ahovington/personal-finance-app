import os

import streamlit as st

from entrypoint.pages.actuals import actuals
from entrypoint.pages.budget import budget
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


# import streamlit as st

# from config import config
# from auth import logout
# from pages import (
#     login_pages,
#     reset_password_pages,
#     finance_pages,
#     registrations_pages,
#     result_pages,
#     selections_pages,
# )


# if __name__ == "__main__":
#     st.set_page_config(
#         page_title="Newcastle West Hockey",
#         page_icon=config.app.club_logo,
#         layout="wide",
#         initial_sidebar_state="auto",
#     )

#     navigation: dict[str : list[st.Page]] = {}
#     if not st.session_state.get("authentication_status", False):
#         navigation["Login"] = login_pages
#     navigation["Results"] = result_pages
#     navigation["Selections"] = selections_pages
#     navigation["Registrations"] = registrations_pages
#     navigation["Finance"] = finance_pages
#     if st.session_state.get("authentication_status", False):
#         navigation["Reset Password"] = reset_password_pages

#     if st.session_state.get("authentication_status", False):
#         logout()

#     pg = st.navigation(navigation)
#     st.logo(config.app.club_logo)
#     col1, col2 = st.columns([1, 6], vertical_alignment="center", gap="medium")
#     col1.image(config.app.club_logo, use_column_width=False, width=100)
#     col2.title(
#         config.app.club_name + " Hockey Club",
#     )
#     st.sidebar.text("Maintained by Alastair 🧑🏻‍💻")

#     pg.run()
