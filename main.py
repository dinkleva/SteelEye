from pydantic import BaseModel, Field
from datetime import datetime
from faker import Faker
from fastapi import FastAPI
import random

fake = Faker()
app = FastAPI()

class TradeDetails(BaseModel):
    buySellIndicator: str = Field(description="A value of BUY for buys, SELL for sells.")
    price: float = Field(description="The price of the Trade.")
    quantity: int = Field(description="The amount of units traded.")

class Trade(BaseModel):
    asset_class: str = Field(description="The asset class of the instrument traded. E.g. Bond, Equity, FX...etc")
    counterparty: str = Field(description="The counterparty the trade was executed with.")
    instrument_id: str = Field(description="The ISIN/ID of the instrument traded. E.g. TSLA, AAPL, AMZN...etc")
    instrument_name: str = Field(description="The name of the instrument traded.")
    trade_date_time: datetime = Field(description="The date-time the Trade was executed")
    trade_details: TradeDetails = Field(description="The details of the trade, i.e. price, quantity")
    trade_id: str = Field(description="The unique ID of the trade")
    trader: str = Field(description="The name of the Trader")



#database for 10 mock trades
alltrades = []

for i in range(100):
    mock_trade = Trade(
    asset_class=fake.random_element(elements=("Bond", "Equity", "FX")),
    counterparty=fake.company(),
    instrument_id=fake.uuid4(),
    instrument_name=fake.company_suffix(),
    trade_date_time=fake.date_time(),
    trade_details=TradeDetails(
        buySellIndicator=fake.random_element(elements=("BUY", "SELL")),
        price=fake.pyfloat(min_value=0, max_value=1000),
        quantity=fake.random_int(min=1, max=100),
    ),
    trade_id=fake.uuid4(),
    trader=fake.name(),
    )
    
    alltrades.append(mock_trade)


# api for list of all trades
@app.get('/alltrades/')
def get_all_trades():
    return alltrades



# api for search by id
@app.get('/alltrades/{trade_id}')
async def get_trade_by_id(trade_id: str):
    for trade in alltrades:
        if trade.trade_id == trade_id:
            return trade

    return {'message': 'trade not found by id'}

# api for searching
@app.get("/alltrades/search/")
async def search(query: str):

    for trade in alltrades:
        if trade.counterparty == query or trade.instrument_id == query or trade.instrument_name == query or trade.trader == query:
            return trade
        
    return {'message': 'not found'}



# api for advance filtering
@app.get('/alltrades/filter_asset/')
async def filter(query: str):
    return [trade for trade in alltrades if trade.asset_class == query]

# api for buySell indicator
@app.get('/alltrades/filter_indicator/')
async def filter(query: str):
    return [trade for trade in alltrades if trade.trade_details.buySellIndicator.lower() == query.lower()]

# api for date
@app.get('/alltrades/filter_date/')
async def filter(start: str = '0000-00-00T00:00:00', end: str = '9999-12-31T23:59:59'):
    start = datetime.fromisoformat(start)
    end = datetime.fromisoformat(end)
    return [trade for trade in alltrades if trade.trade_date_time >= start and trade.trade_date_time <= end]


# api for price
@app.get('/alltrades/filter_price/')
async def filter(min: float=0.0000, max: float=1001.0000):
    return [trade for trade in alltrades if trade.trade_details.price >= min and trade.trade_details.price <= max]



