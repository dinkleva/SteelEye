
For the purpose of this assignment I mocked the schema model using pydantic as given in the assignment detail.

Created 100 dummy data for trades.

I created an endpoint for listing all trades which I stored in a list instead of any database.

For listing all trades in the list(alltrades) I created ('/alltrades/') api.

For searching single trade by id I created ('/alltrades/{trade_id}') api.

For searching counterparty, instrument_id, instrument_name, trader created ('/alltrades/search/') api and checked the query string for the desired
string and returned all trades which met the string query.

For advance filter I have used ('/alltrades/filter_asset/') for asset_class, ('/alltrades/filter_indicator/') for buySellIndicator, ('/alltrades/filter_date/') for filtering date which might be start or end or start and end date to filter. I considered the start date '0000-00-00T00:00:00' and end date '9999-12-31T23:59:59' so that all trades can be fetched using these range.

In the same way I filtered the price as i did in date filtering and created ('/alltrades/filter_price/') 



