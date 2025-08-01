#!/usr/bin/env python
"""
try_a_v02.py (version 0.0.4)

frame 0.3.0
cobotta 0.5.5

Kengo NAKADA:
https://github.com/shimane-dev, https://github.com/kengo-nakada
kengo.nakada@mat.shimane-u.ac.jp, kengo.nakada@gmail.com
"""
# import pytest
import sys
import asyncio
import multiprocessing

import logging

# httpx のログを WARNING レベル以上にする（INFO を抑制）
logging.getLogger("httpx").setLevel(logging.WARNING)

from cobotta2 import Config, MotionMode
from cobotta2.server import AsyncCobottaClient
from x_logger import XLogger


# @pytest.mark.asyncio
async def main():
    # await worker_cobotta1(logger)
    await worker_cobotta1()


async def hand_open(
    client,
    speed: int = None,
    logger: XLogger = None,
):
    # await client.hand_move_H(6, True)
    await client.hand_move_A(30, 100)
    # await asyncio.sleep(3)


async def init(
    client,
    speed: int = None,
    logger: XLogger = None,
):
    await hand_open(client, logger)
    await client.move("P120", speed=speed)  # home
    await client.move("P121", speed=speed)  # home


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
    speed: int = None,
    logger: XLogger = None,
):
    """ """
    await client.move("P122", speed=speed)


async def approach_to_sample(
    client,
    *,
    speed: int = None,
    logger: XLogger = None,
):
    # sample の直上へ
    await client.move("P123", speed=speed)  # もっと近く
    await client.wait_for_complete()


async def move_to_scale(
    client,
    *,
    speed: int = None,
    logger: XLogger = None,
):
    await client.move("P124", speed=speed)  # 持ち上げたところ
    await client.move("P125", speed=speed)  #
    await client.move("P126", speed=speed)  #


async def process_in_shield(
    client,
    *,
    place: bool = False,
    pick: bool = False,
    speed: int | None = None,
    logger: XLogger = None,
):
    """
    風防のなかに突入して place する

    Args:
        client:
        place (bool):
        pick (bool):
        speed (int):
        logger:

    Returns:

    """
    # 突入(風防をまたぐ)
    await client.move("P127", speed=speed)  #

    # in shield
    # Approach
    await client.move("P128", speed=speed)  #  アプローチ手前
    await client.move("P129", speed=speed)  #

    if place:
        # Place
        await client.hand_move_A(30, 100)
        await client.move("P129", path_blend="@0", offset=(0, 0, 5), speed=speed)

    if pick:
        # Pick
        await client.hand_move_H(6, True)
        await asyncio.sleep(3)  # 重要

        # 上にあげる
        await client.move(
            "P129",
            path_blend="@0",
            offset=(0, 0, 30),
            speed=speed,
        )

    new_P130 = [
        276.0450426396214,
        38.839590488460324,
        # 97.69473180302617,
        120,
        177.80716919910708,
        3.5715102321743966,
        -171.31186286176393,
        261.0,
    ]
    await client.move(
        new_P130,
        motion_mode=MotionMode.LINE,
        path_blend="@0",
        offiset=(0, 0, 20),
        speed=speed,
    )
    # 外にひく1
    # await client.move(
    #     "P130",
    #     motion_mode=MotionMode.LINE,
    #     path_blend="@0",
    #     offiset=(0, 0, 30),
    #     speed=speed,
    # )
    # ret = await client.get_current_position()
    # print(ret)
    # sys.exit(-1)

    await client.move(
        "P131",
        motion_mode=MotionMode.LINE,
        path_blend="@0",
        offiset=(0, 0, 25),
        speed=speed,
    )  # ひく(まだ風防のなかに指先がある)

    await client.move(
        "P132",
        motion_mode=MotionMode.LINE,
        path_blend="@0",
        offiset=(0, 0, 25),
        speed=speed,
    )  # ひく(これで一応完全に外)

    # 他のところに行けるような位置まで移動
    await client.move("P133", speed=speed)
    # 外でアームを回転させて home へ移動しようとしている
    await client.move("P134", speed=speed)  # もうすこし安全まで移動


async def reset_scale_zero(
    client,
    *,
    speed: int = None,
    logger: XLogger = None,
):
    """Motion は Line 想定"""
    await client.move("P135", speed=speed)  # 準備
    await client.move("P136", speed=speed)  # 準備

    await client.move("P137", speed=speed)  # ボタンの直情
    # time.sleep(3)

    # === Push Button
    # Motion は line を想定
    await client.move("P138", speed=speed)  # 押す

    # Motion は line を想定
    await client.move("P138", offset=(0, 0, -1), speed=speed)  # 押す
    await client.move("P138", offset=(0, 0, 2), speed=speed)

    await client.move("P139", speed=speed)  # 直情退避
    await client.move("P140", speed=speed)  #


async def worker_cobotta1():
    """"""
    Config.load_yaml("config_cobotta1.yaml")
    logger = XLogger(log_level="info", logger_name=Config.CLIENT_LOGGER_NAME)

    client = AsyncCobottaClient(config=Config, logger=logger)
    await client.reset_error()

    try:
        # speed の入手などには take_arm が必要(アームごとのパラメータなので)
        ret = await client.take_arm()
        if ret is None:
            sys.exit(-1)

        await client.turn_on_motor()
        await client.set_speed(100)

        await hand_open(client)

        client.motion_mode = MotionMode.PTP
        await init(client)  # init

        ########### sample を pick
        await move_to_home(client)
        await approach_to_sample(client)
        await pick_and_place(client, pick=True)  # Pick

        ########### 電子天秤の手前まで
        await move_to_scale(client)
        # input("please input key...")

        ########### Place ############
        client.motion_mode = MotionMode.LINE
        await process_in_shield(client, place=True)  # 電子天秤に突っ込む

        ########### Zero Reset ########
        client.motion_mode = MotionMode.LINE
        await reset_scale_zero(client)  # 電子天秤のゼロリセット

        ########### 電子天秤の手前まで
        await move_to_scale(client)

        ########### 天秤においてあるsampleをとる
        client.motion_mode = MotionMode.LINE
        await hand_open(client)  # 念のため
        await process_in_shield(client, pick=True)  # 電子天秤に突っ込む

        ######### ホームにsampleを返す
        await move_to_home(client)
        await approach_to_sample(client)
        await pick_and_place(client, place=True)

        await move_to_home(client)

    except Exception as e:
        logger.error(f"error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
