from enum import Enum
from tortoise.models import Model
from tortoise.fields import IntField, CharField, FloatField, DatetimeField, CharEnumField

class AuctionStatus(str, Enum):
    ACTIVE = "active"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

class Auction(Model):
    id = IntField(pk=True, generated=True) 
    product_id = CharField(max_length=36)
    seller_id = CharField(max_length=36)
    starting_price = FloatField()
    highest_bid_id = IntField(null=True)
    highest_bid_amount = FloatField(null=True)
    end_time = DatetimeField()
    status = CharEnumField(AuctionStatus, default=AuctionStatus.ACTIVE)  # ✅ Proper enum field
    created_at = DatetimeField(auto_now_add=True)
    updated_at = DatetimeField(auto_now=True)