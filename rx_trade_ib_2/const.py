import logging
from zoneinfo import ZoneInfo

TZ_US_EXCHANGE = ZoneInfo("America/New_York")

LOGGER = logging.getLogger("uvicorn.error")
