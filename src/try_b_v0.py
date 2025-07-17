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
    _logger = XLogger(log_level="info", logger_name=Config.COBOTTA_CLIENT_LOGGER_NAME)

    await worker(_logger)


async def hand_open(client, _logger):
    # await client.hand_move_H(6, True)
    await client.hand_move_A(30, 100)
    # await asyncio.sleep(3)


async def init(client, _logger):
    await hand_open(client, _logger)
    await client.move("P120", bstrOpt="Speed=60")  # home
    await client.move("P121", bstrOpt="Speed=100")  # home


async def pick_and_place(client, place: bool, _logger):

    if place:
        await client.hand_move_A(30, 100)
    else:
        await client.hand_move_H(6, True)
    await asyncio.sleep(3)


async def move_to_home(client, _logger):
    """
    home へ移動

    Args:
        client:
        _logger:

    Returns:

    """
    await client.move("P122", bstrOpt="Speed=100")  # home

    # sample の直上へ
    await client.move("P123", bstrOpt="Speed=65")  # home
    await client.wait_for_complete()

    # 手動でサンプルの位置調整
    await asyncio.sleep(3)


async def move_to_scale(client, _logger):
    await client.move("P124", bstrOpt="Speed=65")  # 持ち上げたところ
    await client.move("P125", bstrOpt="Speed=65")  #
    await client.move("P126", bstrOpt="Speed=65")  #


async def process_in_shield(client, place: bool, _logger):
    """
    風防のなかに突入して place する

    Args:
        client:
        place (bool): Place (True), Pick (False)
        _logger:

    Returns:

    """
    # 突入(風防をまたぐ)
    await client.move("P127", bstrOpt="Speed=50")  #

    # in shield
    # Approach
    await client.move("P128", bstrOpt="Speed=50")  #  アプローチ手前
    await client.move("P129", bstrOpt="Speed=30")  #

    if place:
        # Place
        await client.hand_move_A(30, 100)
        await client.move("@0 P129+(0,0,5)")
    else:
        # Pick
        await client.hand_move_H(6, True)
        await asyncio.sleep(5)
        await client.move("@0 P129+(0,0,10)")

    # 外にひく1
    await client.move("P130+(0,0,10)", bstrOpt="Speed=40")

    await client.move("P131", bstrOpt="Speed=100")  # ひく(まだ風防のなかに指先がある)
    await client.move("P132", bstrOpt="Speed=100")  # ひく(これで一応完全に外)

    # 他のところに行けるような位置まで移動
    await client.move("P133", bstrOpt="Speed=100")  # 外でアームを回転させて home へ移動しようとしている
    await client.move("P134", bstrOpt="Speed=100")  # もうすこし安全まで移動


async def reset_scale_zero(client, _logger):
    """ Motion は Line 想定 """
    _logger.info("=== push button (pre)")

    await client.move("P135", bstrOpt="Speed=100")  # 準備
    await client.move("P136", bstrOpt="Speed=100")  # 準備

    await client.move("P137", bstrOpt="Speed=100")  # ボタンの直情
    # time.sleep(3)

    _logger.info("=== push button")
    # Motion は line を想定
    await client.move("P138", bstrOpt="Speed=30")  # 押す

    # Motion は line を想定
    await client.move("P138+(0,0,-1)", bstrOpt="Speed=30")  # 押す
    await client.move("P138+(0,0,2)", bstrOpt="Speed=30")

    await client.move("P139", bstrOpt="Speed=100")  # 直情退避
    await client.move("P140", bstrOpt="Speed=100")  #


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

        await hand_open(client, _logger)

        client.motion_mode = MotionMode.PTP

        await init(client, _logger)  # init
        await move_to_home(client, _logger)
        await pick_and_place(client, False, _logger)  # Pick

        await move_to_scale(client, _logger)  # 電子天秤の手前まで
        # input("please input key...")

        client.motion_mode = MotionMode.LINE
        await process_in_shield(client, True, _logger)  # 電子天秤に突っ込む

        client.motion_mode = MotionMode.LINE
        await reset_scale_zero(client, _logger)  # 電子天秤のゼロリセット

        await move_to_scale(client, _logger)  # 電子天秤の手前まで

        client.motion_mode = MotionMode.LINE
        await hand_open(client, _logger)
        await process_in_shield(client, False, _logger)  # 電子天秤に突っ込む

        await move_to_home(client, _logger)
        await hand_open(client, _logger)

        # # await release(client, _logger)


    except Exception as e:
        _logger.error(f"error: {e}")


if __name__ == "__main__":
    asyncio.run(main())