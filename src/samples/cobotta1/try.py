#!/usr/bin/env python
"""
素で通しで書く

Kengo NAKADA:
https://github.com/shimane-dev, https://github.com/kengo-nakada
kengo.nakada@mat.shimane-u.ac.jp, kengo.nakada@gmail.com
"""
# import pytest
import asyncio
from pathlib import Path

import logging

# httpx のログを WARNING レベル以上にする（INFO を抑制）
logging.getLogger("httpx").setLevel(logging.WARNING)

from cobotta2 import Config, MotionMode
from cobotta2.server import AsyncCobottaClient
from x_logger import XLogger

HERE = Path(__file__).parent
Config.load_yaml(HERE / "config_cobotta1.yaml")
# Config.load_yaml("config_cobotta1.yaml")

logger = XLogger(log_level="info", logger_name=Config.CLIENT_LOGGER_NAME)


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
