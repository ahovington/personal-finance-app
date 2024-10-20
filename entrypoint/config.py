from decimal import Decimal
from pandantic import BaseModel


class TransactionSchema(BaseModel):
    """The expected schema of a transaction."""

    id: str
    created_date: str
    type: str
    description: str
    category: str
    subcategory: str
    amount: Decimal
    account: str
    status: str
