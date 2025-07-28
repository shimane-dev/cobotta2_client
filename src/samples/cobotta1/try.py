#!/usr/bin/env python
"""
素で通しで書く

Kengo NAKADA:
https://github.com/shimane-dev, https://github.com/kengo-nakada
kengo.nakada@mat.shimane-u.ac.jp, kengo.nakada@gmail.com
"""
# import pytest
import asyncio

import logging

# httpx のログを WARNING レベル以上にする（INFO を抑制）
logging.getLogger("httpx").setLevel(logging.WARNING)

from cobotta2.config import Config
from cobotta2.server_fastapi.clients import AsyncCobottaClient
from cobotta2.server_fastapi.models.motion import MotionMode
from x_logger import XLogger

Config.load_yaml("config_server1.yaml")
logger = XLogger(log_level="info", logger_name=Config.COBOTTA_CLIENT_LOGGER_NAME)


# @pytest.mark.asyncio
async def main():
    await worker(logger)


async def worker(_logger):
    """"""
    client = AsyncCobottaClient(config=Config, logger=_logger)
    await client.reset_error()

    try:
        # speed の入手などには take_arm が必要(アームごとのパラメータなので)
        await client.take_arm()
        await client.turn_on_motor()

        client.motion_mode = MotionMode.PTP
        await client.move("P120")  # home
        await client.move("P121")  # home

    except Exception as e:
        _logger.error(f"error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
