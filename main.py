import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from rx_trade_ib_2.options.data.main import get_option_chain
from rx_trade_ib_2.options.data.type.request import OptionChainRequest
from rx_trade_ib_2.options.data.type.response import OptionChainResponse
from rx_trade_ib_2.options.gex.main import calc_gex_stats
from rx_trade_ib_2.options.gex.request import OptionsGexStatsRequest
from rx_trade_ib_2.options.gex.response import OptionsGexStatsResponse

app = FastAPI()
# noinspection PyTypeChecker
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:3388",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/options/gex", response_model=OptionsGexStatsResponse)
async def option_gex(request: OptionsGexStatsRequest):
    return calc_gex_stats(request)


@app.post("/options/chain", response_model=OptionChainResponse)
async def option_chain(request: OptionChainRequest):
    return get_option_chain(request)


if __name__ == '__main__':
    uvicorn.run(app, port=6284)
