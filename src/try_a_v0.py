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
_logger = XLogger(log_level="info", logger_name=Config.COBOTTA_CLIENT_LOGGER_NAME)


# @pytest.mark.asyncio
async def main():
    await worker(_logger)


async def pick(client, _logger):
    await client.move("P122", bstrOpt="Speed=50")  # home
    await client.hand_move_A(30, 100)
    await client.wait_for_complete()

    await client.move("P123", bstrOpt="Speed=30")  # home
    await client.wait_for_complete()

    # input("何かキーを押してください...")
    await asyncio.sleep(5)

    await client.hand_move_H(6, True)
    await asyncio.sleep(3)


async def release(client, _logger):
    await client.move("P122", bstrOpt="Speed=50")  # home
    await client.move("P123", bstrOpt="Speed=30")  # home
    await client.hand_move_A(30, 100)
    await asyncio.sleep(5)


async def worker(_logger):
    """"""
    client = AsyncCobottaClient(config=Config, logger=_logger)
    await client.reset_error()

    try:
        # speed の入手などには take_arm が必要(アームごとのパラメータなので)
        await client.take_arm()
        await client.turn_on_motor()

        client.motion_mode = MotionMode.PTP
        await client.move("P120", bstrOpt="Speed=50")  # home
        await client.move("P121", bstrOpt="Speed=50")  # home

        ################ Pick
        await pick(client, _logger)
        ################

        await client.move("P124", bstrOpt="Speed=40")  # 持ち上げたところ
        await client.move("P125", bstrOpt="Speed=40")  #
        await client.move("P126", bstrOpt="Speed=40")  #
        # input("何かキーを押してください...")
        # time.sleep(4)

        client.motion_mode = MotionMode.LINE
        await client.move("P127", bstrOpt="Speed=40")  # home

        ############### 中

        # Approach
        await client.move("P128", bstrOpt="Speed=30")  # home ## アプローチ手前

        await client.move("P129", bstrOpt="Speed=30")  #
        # Place
        await client.hand_move_A(30, 100)

        await client.move("P130", bstrOpt="Speed=40")  # 外にひく1

        await client.move("P131", bstrOpt="Speed=40")  # ひく
        await client.move("P132", bstrOpt="Speed=40")  #
        await client.move("P133", bstrOpt="Speed=40")  #
        await client.move("P134", bstrOpt="Speed=40")  #
        # 外に出て release に LINE でいける所

        _logger.info("===release")
        client.motion_mode = MotionMode.PTP

        #################
        # await release(client, _logger)
        #################

        _logger.info("=== push button (pre)")

        await client.move("P135", bstrOpt="Speed=50")  # 準備
        await client.move("P136", bstrOpt="Speed=50")  # 準備

        await client.move("P137", bstrOpt="Speed=30")  # ボタンの直情
        # time.sleep(3)

        _logger.info("=== push button")
        await client.move("P138", bstrOpt="Speed=30")  # 押す
        client.motion_mode = MotionMode.LINE
        await client.move("P138+(0,0,-1)", bstrOpt="Speed=30")  # 押す
        await client.move("P138+(0,0,2)", bstrOpt="Speed=30")

        await client.move("P139", bstrOpt="Speed=30")  # 直情退避
        await client.move("P140", bstrOpt="Speed=30")  #

    except Exception as e:
        _logger.error(f"error: {e}")


if __name__ == "__main__":
    asyncio.run(main())