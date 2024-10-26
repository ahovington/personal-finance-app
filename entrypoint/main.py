import os

from app import BudgetPlanner, budget_app
from mockdata import BudgetDataMock
from upbank import BudgetDataUp, UpbankClient

DATABASE_CONNECTION = "./db/db.duckdb"
UPBANK_TOKEN = os.getenv("UPBANK_TOKEN")
IS_MOCK_DATA = os.getenv("IS_MOCK_DATA", False)

generator = BudgetDataMock()
if not IS_MOCK_DATA:
    client = UpbankClient(os.getenv("UPBANK_TOKEN"))
    generator = BudgetDataUp(client, DATABASE_CONNECTION)

planner = BudgetPlanner()
budget_app(generator, planner)
