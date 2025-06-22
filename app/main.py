from sanic import Sanic , response
from sanic.response import json
from sanic.request import Request
from sanic.exceptions import InvalidUsage  , Unauthorized
import httpx
from pydantic import BaseModel, field_validator , Field
from datetime import datetime
from app.models.auction import Auction  # Import model
from app.db import init_db

 
app = Sanic("HelloWorldApp")

init_db(app)  # Initialize database
class CreateAuctionInput(BaseModel):
    product_id: str
    starting_price: float
    end_time: datetime = Field(..., alias="endtime")

    @field_validator("product_id")
    @classmethod
    def validate_product_id(cls, v: str) -> str:
        if not isinstance(v, str) or not v.strip():
            raise InvalidUsage("Invalid product_id: must be a non-empty string")
        return v

    @field_validator("starting_price")  
    @classmethod
    def validate_starting_price(cls, v: float) -> float:
        if v <= 0:
            raise InvalidUsage("Invalid starting_price")
        return v

    @field_validator("end_time")
    @classmethod
    def validate_end_time(cls, v: datetime) -> datetime:
        if v <= datetime.utcnow():
            raise InvalidUsage("Invalid end_time")
        return v
    
    
    
async def json_response(success: bool, data=None, error=None, status=200):
    return response.json(
        {"success": success, "data": data, "error": error, },
        status=status,
    )
# Middleware to validate session
@app.middleware("request")
async def validate_session(request: Request):
    if request.path != "/":
        # Check for both secure and non-secure NextAuth cookies
        cookie_name = "__Secure-next-auth.session-token"
        cookie_value = request.cookies.get(cookie_name)
        if not cookie_value:
            cookie_name = "next-auth.session-token"
            cookie_value = request.cookies.get(cookie_name)
        if not cookie_value:
            raise Unauthorized("No session cookies provided")
        cookies = {cookie_name: cookie_value}
        print(f"Forwarding cookies: {cookies}")  # Debug logging
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get(
                    "https://ecokartuk.com/api/auth/session",
                    cookies=cookies,
                    timeout=5,
                )
             
                user_data = resp.json()
                print(f"Session response: {user_data}")  # Debug logging
                request.ctx.user = {
                    "id": user_data["user"]["id"],
                    "role": user_data["user"]["role"],
                    "email": user_data["user"].get("email"),
                }
            except httpx.HTTPError as e:
                raise Unauthorized(f"Failed to validate session: {str(e)}")

    
# get route and frontend
@app.route("/")
async def hello(request):
    return await json_response(True, {"message": "Auction service is running"})

# get this from the create-auction
@app.route("/create-auction", methods=["POST"])
async def create_auction(request: Request):
    try:
        print(request.json , "eorkj fasfsd")
        # Validate input
        data = CreateAuctionInput(**request.json)
        
        print(data , "check the data")
        # Check for existing active auction
        existing_auction = await Auction.filter(
            product_id=data.product_id, status="active"
        ).exists() 
        if existing_auction:
            return await json_response(
                False, error="An active auction already exists for this product", status=400
            )

        # Create auction
        auction = await Auction.create(
            product_id=data.product_id,
            seller_id=request.ctx.user["id"],
            starting_price=data.starting_price,
            end_time=data.end_time,
            status="active",
        )
        
        print(auction , "working")

        return await json_response(
            True,
            {
                "message": "Auction created successfully",
                "data": {
                    "id": auction.id,
                    "product_id": auction.product_id,
                    "seller_id": auction.seller_id,
                    "starting_price": auction.starting_price,
                    "end_time": str(auction.end_time),
                    "status": auction.status,
                },
            },
            status=201,
        )

    except InvalidUsage as e:
        return await json_response(False, error=str(e), status=400)
    except ValueError as e:
        return await json_response(False, error=str(e), status=400)
    except Unauthorized as e:
        return await json_response(False, error=str(e), status=401)
    except Exception as e:
        return await json_response(False, error=str(e), status=500)

@app.route("/get-auction-by-product-id/<product_id:str>", methods=["GET"])
async def get_auction_by_product_id(request: Request, product_id: str):
    try:
        if not product_id:
            return await json_response(False, error="Product ID is required", status=400)
        auction = await Auction.filter(product_id=product_id , status="active").first() 
        if not auction:
            return await json_response(False, error="Auction not found", status=404)

        return await json_response(
            True,
            {
                "id": auction.id,
                "product_id": auction.product_id,
                "seller_id": auction.seller_id,
                "starting_price": auction.starting_price,
                "end_time": str(auction.end_time),
                "status": auction.status,
            },
            status=200,
        )

    except Exception as e:
        return await json_response(False, error=str(e), status=500)
    
    
    
    
     
    

#get by primery key  
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