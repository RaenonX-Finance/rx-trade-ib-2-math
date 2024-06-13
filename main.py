import uvicorn
from fastapi import FastAPI

from rx_trade_ib_2.options.gex.main import calc_gex_stats
from rx_trade_ib_2.options.gex.request import OptionsGexStatsRequest
from rx_trade_ib_2.options.gex.response import OptionsGexStatsResponse

app = FastAPI()


@app.post("/options/gex", response_model=OptionsGexStatsResponse)
async def gex(request: OptionsGexStatsRequest):
    return calc_gex_stats(request)


if __name__ == '__main__':
    uvicorn.run(app, port=6284)
