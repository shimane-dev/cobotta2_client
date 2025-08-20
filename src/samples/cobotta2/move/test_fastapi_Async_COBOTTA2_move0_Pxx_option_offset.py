#!/usr/bin/env python
"""
内部変数値を読んで、それを配列に入れなおして、そこに移動する

Kengo NAKADA:
https://github.com/shimane-dev, https://github.com/kengo-nakada
kengo.nakada@mat.shimane-u.ac.jp, kengo.nakada@gmail.com
"""
import pytest

from cobotta2.server_fastapi.clients.async_cobotta_state_client import (
    AsyncCobottaStateClient,
)


@pytest.mark.asyncio
async def test_fastapi_Async_move2_P2():
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

    # speed の入手などには take_arm が必要(アームごとのパラメータなので)
    logger.info("take_arm")
    ret = await client.take_arm()
    assert ret is not None, "Connect Error"

    logger.info("turn_on_motor")
    ret = await client.turn_on_motor()

    logger.info(f"motion_mode = {MotionMode.PTP}")
    client.motion_mode = MotionMode.PTP

    num = f"P{110}"
    ret = await client.get_P(f"{num}")
    logger.info(f"== move({num}: {ret})")

    # ret = await client.move(f"@E {num}+(-12,-22,0)", bstrOpt=30)
    await client.move(f"@E {num}", speed=30)
    await client.move(f"@0 {num}", offset=(0, 0, 50), speed=30)
    await client.wait_for_complete()

    assert ret is not None, "接続失敗"

    current_pos = await client.get_current_position()
    logger.info(f"current_position: {current_pos}")
    assert "result" == "result"
