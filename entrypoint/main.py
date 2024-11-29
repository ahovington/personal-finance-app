import os

from budget_actuals import BudgetPlanner, actuals
from mockdata import BudgetDataMock
from upbank import BudgetDataUp, UpbankClient

DATABASE_CONNECTION = "./db/db.duckdb"
UPBANK_TOKEN = os.getenv("UPBANK_TOKEN")
IS_MOCK_DATA = os.getenv("IS_MOCK_DATA", False)
REFRESH_DATA = os.getenv("REFRESH_DATA", False)  # THIS Needs to be a button somewhere.

if IS_MOCK_DATA:
    generator = BudgetDataMock()
else:
    client = UpbankClient(UPBANK_TOKEN)
    generator = BudgetDataUp(client, DATABASE_CONNECTION)


planner = BudgetPlanner()
actuals(generator, planner)
