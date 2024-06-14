import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from rx_trade_ib_2.options.gex.main import calc_gex_stats
from rx_trade_ib_2.options.gex.request import OptionsGexStatsRequest
from rx_trade_ib_2.options.gex.response import OptionsGexStatsResponse

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:3100",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/options/gex", response_model=OptionsGexStatsResponse)
async def gex(request: OptionsGexStatsRequest):
    return calc_gex_stats(request)


if __name__ == '__main__':
    uvicorn.run(app, port=6284)
