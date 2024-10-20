from decimal import Decimal
from pandantic import BaseModel
from enum import StrEnum


class TransactionTypes(StrEnum):
    INCOME = "Income"
    PURCHASE = "Purchase"


class TransactionSchema(BaseModel):
    """The expected schema of a transaction."""

    id: str
    created_date: str
    type: str
    description: str
    type: TransactionTypes
    category: str
    subcategory: str
    amount: Decimal
    account: str
    status: str
