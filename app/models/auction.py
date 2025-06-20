from tortoise import fields
from tortoise.models import Model


class Auction(Model):
    id = fields.IntField(pk=True)
    product_id = fields.CharField(max_length=100)
    starting_price = fields.FloatField()
    end_time = fields.DatetimeField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)    