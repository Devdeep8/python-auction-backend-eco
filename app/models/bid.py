from tortoise.models import Model
from tortoise.fields import IntField, CharField, FloatField, DatetimeField, ForeignKeyField

class Bid(Model):
    id = IntField(pk=True)  # Auto-incrementing primary key
    auction = ForeignKeyField("models.Auction", related_name="bids")  # Foreign key to Auction
    user_id = CharField(max_length=36)  # Optional integer user ID (if needed)
    bid_amount = FloatField()  # Amount of the bid
    status = CharField(max_length=20, default="accepted")  # Bid status: accepted, outbid, rejected
    created_at = DatetimeField(auto_now_add=True)  # Timestamp when bid is placed
    updated_at = DatetimeField(auto_now=True)  # Timestamp for updates

    class Meta:
        table = "bid"  # Explicit table name