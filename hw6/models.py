"""The public answer schema: null means a fact was absent or ambiguous."""
from typing import Literal
from pydantic import BaseModel, Field, ConfigDict


class QuoteFacts(BaseModel):
    model_config = ConfigDict(extra='forbid')
    vendor: str | None = Field(description='Vendor name stated in this quote, not its email sender name.')
    sku: str | None = Field(description='Campus Customs SKU in the quote.')
    unit_price: float | None = Field(ge=0, description='Quoted dollars per unit, without changing the quote.')
    lead_time_days: int | None = Field(ge=0, description='Stated lead time in days.')
    min_order: int | None = Field(ge=0, description='Stated minimum order quantity in units.')


class VendorDecision(QuoteFacts):
    decision: Literal['recommend', 'do_not_recommend']
    reason: str = Field(description='One sentence explaining the relevant handbook purchasing checks.')
