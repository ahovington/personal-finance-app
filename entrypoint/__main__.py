import os

from .mockdata import BudgetDataMock
from .upbank import UpbankClient, BudgetDataUp
from .app import BudgetPlanner, budget_app


DATABASE_CONNECTION = "./db/db.duckdb"
UPBANK_TOKEN = os.getenv("UPBANK_TOKEN")
IS_MOCK_DATA = os.getenv("IS_MOCK_DATA", True)

generator = BudgetDataMock()
if not IS_MOCK_DATA:
    client = UpbankClient(os.getenv("UPBANK_TOKEN"))
    generator = BudgetDataUp(client, DATABASE_CONNECTION)

planner = BudgetPlanner(generator)
budget_app(generator, planner)

# print(
#     ddb.sql(
#         """
#         select
#             type,
#             id,
#             attributes.settledAt as settledAt,
#             attributes.createdAt as createdAt,
#             attributes.transactionType as transactionType,
#             attributes.rawText as rawText,
#             attributes.description as description,
#             attributes.isCategorizable as isCategorizable,
#             attributes.amount.currencyCode as currencyCode,
#             attributes.amount.value as value,
#             attributes.amount.valueInBaseUnits as valueInBaseUnits,
#             attributes.note.text as noteText,
#             attributes.performingCustomer.displayName as performingCustomer,
#             relationships.transferAccount as transferAccount,
#             relationships.category.data.id as category,
#             relationships.parentCategory.data.id parentCategory,
#             relationships.tags.data as tags
#         from transactions
#     """
#     )
# )

# print(
#     ddb.sql(
#         """
#         select
#             attributes.createdAt as created_ts,
#             attributes.displayName as display_name,
#             attributes.accountType as account_type,
#             attributes.ownershipType as ownership_type,
#             cast(attributes.balance.value as DECIMAL) as balance
#             cast(attributes.balance.valueInBaseUnits as DECIMAL) as balance_base_units
#         from accounts
#     """
#     )
# )
