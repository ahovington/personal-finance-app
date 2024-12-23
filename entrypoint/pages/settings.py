import streamlit as st

from sources.mockdata import BudgetDataMock


if __name__ == "__main__":
    # Generate sample transactions
    budget_data = BudgetDataMock()

    st.title("Settings")

    st.divider()
    refresh_containter = st.container(border=True)
    refresh_containter.subheader("Refresh budget data")
    refresh_trans = refresh_containter.button(
        "Refresh transactions",
        on_click=budget_data.refresh_transactions(),
        use_container_width=True,
    )
    # if refresh_trans:
    #     refresh_containter.write("Refreshing transactions..")
    #     budget_data.refresh_transactions()
    refresh_acc = refresh_containter.button(
        "Refresh accounts",
        on_click=budget_data.refresh_accounts(),
        use_container_width=True,
    )
    # if refresh_acc:
    #     refresh_containter.write("Refreshing accounts..")
    #     budget_data.refresh_accounts()
