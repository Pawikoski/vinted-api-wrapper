from dataclasses import dataclass
from typing import Optional


@dataclass
class MethodPay:
    id: int
    code: Optional[str]
    requires_credit_card: Optional[bool]
    event_tracking_code: Optional[str]
    icon: Optional[str]
    enabled: Optional[bool]
    translated_name: Optional[str]
    note: Optional[str]
    method_change_possible: bool


@dataclass
class CurrencyAmount:
    amount: Optional[str]
    currency_code: Optional[str]


@dataclass
class Conversion:
    seller_price: Optional[str]
    seller_currency: Optional[str]
    buyer_currency: Optional[str]
    fx_rounded_rate: Optional[str]
    fx_base_amount: Optional[str]
    fx_markup_rate: Optional[str]


@dataclass
class Price:
    amount: Optional[str]
    currency_code: Optional[str]
