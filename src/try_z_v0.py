#!/usr/bin/env python
"""
部品化して再利用できるように書く
(ただし結局座標は一点もの)

Kengo NAKADA:
https://github.com/shimane-dev, https://github.com/kengo-nakada
kengo.nakada@mat.shimane-u.ac.jp, kengo.nakada@gmail.com
"""
# import pytest
import asyncio
import multiprocessing

import logging

# httpx のログを WARNING レベル以上にする（INFO を抑制）
logging.getLogger("httpx").setLevel(logging.WARNING)

from cobotta2.config import Config
from cobotta2.server_fastapi.clients import AsyncCobottaClient
from cobotta2.server_fastapi.models.motion import MotionMode
from x_logger import XLogger


# @pytest.mark.asyncio
async def main():
    Config.load_yaml("config_server1.yaml")
    logger = XLogger(log_level="info", logger_name=Config.CLIENT_LOGGER_NAME)

    await worker(logger)


async def hand_open(
    client,
    logger: XLogger = None,
):
    # await client.hand_move_H(6, True)
    await client.hand_move_A(30, 100)
    # await asyncio.sleep(3)


async def init(
    client,
    logger: XLogger = None,
):
    await hand_open(client, logger)
    await client.move("P120", bstrOpt="Speed=60")  # home
    await client.move("P121", bstrOpt="Speed=100")  # home


async def pick_and_place(
    client,
    place: bool = False,
    pick: bool = False,
    logger: XLogger = None,
):
    if place:
        await client.hand_move_A(30, 100)

    if pick:
        await client.hand_move_H(6, True)
    await asyncio.sleep(3)


async def move_to_home(
    client,
    *,
    logger: XLogger = None,
):
    """ """
    await client.move("P122", bstrOpt="Speed=100")


async def worker(_logger):
    """"""
    client = AsyncCobottaClient(config=Config, logger=_logger)
    await client.reset_error()

    try:
        # speed の入手などには take_arm が必要(アームごとのパラメータなので)
        await client.take_arm()
        await client.turn_on_motor()

        # await hand_open(client, _logger)

        # client.motion_mode = MotionMode.PTP
        # await init(client, _logger)  # init

        await move_to_home(client)
        await client.move_L("P122+(0,0,150)", bstrOpt="Speed=40")
        # await client.move_P("P122+(0,50,150)", bstrOpt="Speed=40")

    except Exception as e:
        _logger.error(f"error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
