from sanic import Sanic
from sanic.response import json
from sanic.request import Request
from sanic.exceptions import InvalidUsage
from app.models.auction import Auction  # Import model

from app.db import init_db

app = Sanic("HelloWorldApp")
init_db(app)

@app.route("/")
async def hello(request):
    return json({"message": "Deva can do the best possible in this world"})


@app.route("/create-auction", methods=["POST"])
async def create_auction(request: Request):
    try:
        data = request.json
        if not data:
            raise InvalidUsage("No data provided", status_code=400)

        product_id = data.get("product_id")
        starting_price = data.get("starting_price")
        end_time = data.get("end_time")

        if not product_id or not starting_price or not end_time:
            raise InvalidUsage("Missing required fields: product_id, starting_price, end_time")

        # ✅ Save to DB
        auction = await Auction.create(
            product_id=product_id,
            starting_price=starting_price,
            end_time=end_time
        )

        return json({
            "success": True,
            "message": "Auction created successfully",
            "data": {
                "id": auction.id,
                "product_id": auction.product_id,
                "starting_price": auction.starting_price,
                "end_time": str(auction.end_time)
            }
        }, status=201)

    except InvalidUsage as e:
        return json({"success": False, "error": str(e)}, status=400)
    except Exception as e:
        return json({"success": False, "error": str(e)}, status=500)



@app.route("/get-auction/auction/<auction_id:int>"  , methods=["GET"])
async def get_auction_by_id(request : Request , auction_id : int):
    try:
        auction = await Auction.get(id = auction_id)
        if not auction:
            return json({"success": False, "error": "Auction not found"}, status=404)
        
        return json({
             "success": True,
            "data": {
                "id": auction.id,
                "product_id": auction.product_id,
                "starting_price": auction.starting_price,
                "end_time": str(auction.end_time),
                "created_at": str(auction.created_at),
                "updated_at": str(auction.updated_at),
            }
        })
    except Exception as e:
        return json({"success": False, "error": str(e)}, status=500)    