#!/usr/bin/env python
"""
内部変数値を読んで、それを配列に入れなおして、そこに移動する

Kengo NAKADA:
https://github.com/shimane-dev, https://github.com/kengo-nakada
kengo.nakada@mat.shimane-u.ac.jp, kengo.nakada@gmail.com
"""
import pytest


@pytest.mark.asyncio
async def test_fastapi_Async_move2_P2():
    import logging
    import asyncio
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

    # await client.reset_error()

    # speed の入手などには take_arm が必要(アームごとのパラメータなので)
    logger.info("take_arm")
    ret = await client.take_arm()
    assert ret is not None, "接続失敗"

    logger.info("turn_on_motor")
    ret = await client.turn_on_motor()
    assert ret is not None, "接続失敗"

    logger.info(f"motion_mode = {MotionMode.PTP}")
    client.motion_mode = MotionMode.PTP

    # ret = await client.get_P(f"P110")
    # logger.info(f"== move(): {ret})")

    # ret = await client.move(f"P110", bstrOpt=50)
    # await client.move_L(f"P110", path_blend="@P", speed=50)
    # await client.move_L(f"P111", speed=50)
    # await client.move_L(f"P112", speed=50)
    # await client.wait_for_complete()
    # await client.move_L(f"P111", speed=50)
    # await client.move_L(f"P110", speed=50)
    # await client.wait_for_complete()
    # await client.move_L(f"P110", offset=(0, 0, 20), speed=50)

    # await client.set_speed(100)
    # await client.move_L(f"P110", path_blend="@P")
    # await client.move_L(f"P111")
    # await client.move_L(f"P112")
    # await client.wait_for_complete()
    # await client.move_L(f"P111")
    # await client.move_L(f"P110")
    # await client.wait_for_complete()
    # await client.move_L(f"P110", offset=(0, 0, 20))

    await client.set_speed(100)
    await client.set_path_blend("@0")
    await client.move_L(f"P110")
    await client.move_L(f"P111")
    await client.move_L(f"P112")
    await client.wait_for_complete()
    await client.move_L(f"P111")
    await client.move_L(f"P110")
    await client.wait_for_complete()
    await client.move_L(f"P110", path_blend="@P", offset=(0, 0, 10))

    current_pos = await client.get_current_position()
    logger.info(f"current_position: {current_pos}")
    assert "result" == "result"
