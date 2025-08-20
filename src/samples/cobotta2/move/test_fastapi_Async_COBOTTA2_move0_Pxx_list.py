#!/usr/bin/env python
"""
内部変数値を読んで、それを配列に入れなおして、そこに移動する

Kengo NAKADA:
https://github.com/shimane-dev, https://github.com/kengo-nakada
kengo.nakada@mat.shimane-u.ac.jp, kengo.nakada@gmail.com
"""
import pytest
from cobotta2.server import AsyncCobottaClient


@pytest.mark.asyncio
async def test():
    import logging
    from pathlib import Path

    # httpx のログを WARNING レベル以上にする（INFO を抑制）
    logging.getLogger("httpx").setLevel(logging.WARNING)

    from cobotta2 import Config, MotionMode
    from cobotta2.server import AsyncCobottaClient
    from x_logger import XLogger

    HERE = Path(__file__).parent
    Config.load_yaml(HERE / "../config_cobotta2.yaml")
    # Config.load_yaml("../config_cobotta2.yaml")

    logger = XLogger(log_level="info", logger_name=Config.CLIENT_LOGGER_NAME)
    client = AsyncCobottaClient(config=Config, logger=logger)
    await client.reset_error()

    logger.info("turn_on_motor")
    await client.turn_on_motor()

    # speed の入手などには take_arm が必要(アームごとのパラメータなので)
    logger.info("take_arm")
    ret = await client.take_arm()

    logger.info(f"motion_mode = {MotionMode.PTP}")
    client.motion_mode = MotionMode.PTP

    ret = await client.get_P(f"P110")
    logger.info(f"== get_P(): {ret})")

    # # ret = await client.move("P110")
    # P110_camera = (
    #     197.74189325511722,  # X
    #     -102.87065719423421,  # y
    #     # 45.40395449388056,  # z
    #     180.0,  # z
    #     -176.46837944742447,  # rx
    #     # 10.232977777915506,  # ry
    #     0.0,
    #     176.76296478619867,  # rz
    #     261.0,
    # )
    # ret = await client.move(P110_camera, speed=50)

    # await client.move("P110", speed=50)
    # ret = await client.move(f"@E {num}+(-12,-22,0)", bstrOpt=30)

    await client.move(ret, speed=50)
    await client.wait_for_complete()

    # assert ret is not None, "接続失敗"

    # current_pos = await client.get_current_position()
    # logger.info(f"current_position: {current_pos}")
    assert "result" == "result"
