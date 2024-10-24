"""Up Bank API.

Use the Up Bank API to retrieve transactions.
"""

import datetime
import json
from enum import StrEnum
from pathlib import Path

import duckdb
import requests

from config import TransactionSchema

URL = "https://api.up.com.au/api/v1"

# Maximum number of transactions upbank return per 'page'.
PAGE_SIZE = 100


class TransactionStatus(StrEnum):
    HELD = "HELD"
    SETTLED = "SETTLED"


class UpbankClient:
    def __init__(self, token: str):
        """
        token: str: upbank "personal access token" from https://api.up.com.au/getting_started
        """
        self.token = token

    def transactions(
        self,
        since: datetime.datetime,
        until: datetime.date | None = None,
        status: TransactionStatus | None = None,
    ) -> list:
        """Fetch a list of transactions.

        Args:
            since: tzaware datetime to start from
            until: tzaware datetime to stop at; or None for all.
            status: "HELD" or "SETTLED"

        Returns:
            list of "SETTLED" transactions in dict format.
        """
        params = dict()

        # Upbank only return PAGE_SIZE transactions per request, so we need to
        params.update({"page[size]": PAGE_SIZE})
        params.update({"filter[since]": since})
        if until is not None:
            params.update({"filter[until]": until})
        if status is not None:
            params.update({"filter[status]": status})
        response = self.get("/transactions", params=params)
        return response

    def get(self, path, params: dict = None) -> list:
        """Send a GET request to Up.

        Args:
            path: includes the preceding slash.
            params: request parameters.

        Returns:
            list of data; probably dicts.
        """
        result = []
        uri = f"{URL}{path}"
        while uri is not None:
            response = requests.get(uri, headers=self._headers(), params=params)
            data = response.json()
            result.extend(data["data"])
            try:
                uri = data["links"]["next"]
            except KeyError:
                break
        return result

    def ping(self):
        """Verify the access token is working.

        Returns:
            requests.Response
        """
        return requests.get(f"{URL}/util/ping", headers=self._headers())

    def accounts(self):
        """Fetch a list of accounts."""
        return self.get("/accounts")

    def categories(self):
        """Fetch a list of categories."""
        return self.get("/categories")

    def _headers(self):
        return {"Authorization": f"Bearer {self.token}"}


class BudgetDataUp:

    def __init__(
        self, api_client: UpbankClient, database_connection: str = "./db/db.duckdb"
    ):
        self.client = api_client
        self.conn = duckdb.connect(database=Path(database_connection), read_only=False)

    def refresh_categories(self):
        """Get a list of transaction categories."""
        # TODO: Implement
        # response = client.categories()
        # pprint.pformat(response)

    def refresh_accounts(self):
        """Fetch the current balance of the account."""
        response = self.client.accounts()
        with open(Path("./db/accounts.json"), "w", encoding="utf-8") as f:
            json.dump(response, f, ensure_ascii=False, indent=4)
        self.conn.sql(
            """
            create table accounts as (
                select *
                from read_json_auto('./db/accounts.json')
            )
            """
        )

    def refresh_transactions(self):
        """Download held transactions."""
        local_tz = datetime.datetime.now().astimezone().tzinfo
        now = datetime.datetime.now().replace(tzinfo=local_tz)
        since = now - datetime.timedelta(days=365)
        response = self.client.transactions(since, status=TransactionStatus.SETTLED)
        with open(Path("./db/transactions.json"), "w", encoding="utf-8") as f:
            json.dump(response, f, ensure_ascii=False, indent=4)
        self.conn.sql(
            """
            create or replace table transactions as (
                select *
                from read_json_auto('./db/transactions.json')
            )
        """
        )

    def get_transactions(
        self,
        start_date: datetime,
        end_date: datetime,
        validate_transactions: bool = True,
    ):

        transaction = {
            "id": self.fake.uuid4(),
            "created_date": current_date.strftime("%Y-%m-%d"),
            "description": f"{self.fake.company()} - {subcategory}",
            "type": (
                TransactionTypes.INCOME
                if category == "Income"
                else TransactionTypes.PURCHASE
            ),
            "category": category,
            "subcategory": subcategory,
            "amount": round(random.uniform(*amount_range), 2),
            "account": random.choice(["Checking", "Credit Card", "Cash"]),
            "status": random.choice(["cleared", "pending"]),
        }
        if validate_transactions:
            self._validate_transactions(df)
        return df

    def _validate_transactions(self, df):
        # validate transactions
        return TransactionSchema.parse_df(
            dataframe=df,
            errors="raise",
        )


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
