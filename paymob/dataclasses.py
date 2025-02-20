from datetime import datetime
from unittest.mock import Base
from pydantic import BaseModel, Field, HttpUrl, model_validator, ValidationError
from typing import Any, List, Optional, Dict, Union
import requests
import hmac
import hashlib

# --------------------------
# Data Classes
# --------------------------

class Item(BaseModel):
    name: str
    amount: int
    description: str
    quantity: int

class BillingData(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    email: str
    apartment: str = "dumy"
    street: str = "dumy"
    building: str = "dumy"
    city: str = "dumy"
    country: str = "dumy"
    floor: str = "dumy"
    state: str = "dumy"


class Intention(BaseModel):
    amount: int
    currency: str = "EGP"
    payment_methods: List[Union[str,int]]
    items: List[Item] = []
    billing_data: BillingData
    special_reference: str
    notification_url: str
    redirection_url: str
    extras: Dict[str, Any] = Field(default_factory=dict)

    # @model_validator(mode='after')
    # def validate_amount(self) -> 'Intention':
    #     total_amount = sum(item.amount for item in self.items)
    #     if total_amount != self.amount:
    #         raise ValueError(
    #             f"Total items amount {total_amount} doesn't match "
    #             f"specified amount {self.amount}"
    #         )
    #     return self


class PaymentKey(BaseModel):
    integration: int
    key: str
    gateway_type: str
    iframe_id: Optional[str] = None
    order_id: int
    redirection_url: HttpUrl
    save_card: bool


class ResponseBillingData(BaseModel):
    apartment: str
    floor: str
    first_name: str
    last_name: str
    street: str
    building: str
    phone_number: str
    shipping_method: str
    city: str
    country: str
    state: str
    email: str
    postal_code: str


class IntentionDetail(BaseModel):
    amount: int
    items: List[Item] 
    currency: str
    billing_data: ResponseBillingData


class PaymentMethod(BaseModel):
    integration_id: int
    alias: Optional[str] = None
    name: Optional[str] = None
    method_type: str
    currency: str
    live: bool
    use_cvc_with_moto: bool


class CreationExtras(BaseModel):
    merchant_order_id: Optional[str] = None


class Extras(BaseModel):
    creation_extras: CreationExtras
    confirmation_extras: Optional[Dict[str, Any]] = None


class PaymentIntention(BaseModel):
    payment_keys: List[PaymentKey]
    redirection_url: HttpUrl
    intention_order_id: int
    id: str
    intention_detail: IntentionDetail
    client_secret: str
    payment_methods: List[PaymentMethod]
    special_reference: str
    extras: Extras
    confirmed: bool
    status: str
    created: datetime
    card_detail: Optional[Dict[str, Any]] = None
    card_tokens: List[Dict[str, Any]] = Field(default_factory=list)
    object: str


class Errors(BaseModel):
    errors:dict = Field(default_factory=dict) 