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
async def test():
    import logging

    # httpx のログを WARNING レベル以上にする（INFO を抑制）
    logging.getLogger("httpx").setLevel(logging.WARNING)

    from cobotta2.config import Config
    from cobotta2.server_fastapi.clients import AsyncCobottaClient
    from cobotta2.server_fastapi.models.motion import MotionMode
    from x_logger.x_logger import XLogger

    Config.load_yaml("../config_server2.yaml")
    Config.load_yaml("../config_server2_state.yaml")

    logger = XLogger(log_level="info", logger_name=Config.COBOTTA_CLIENT_LOGGER_NAME)
    state = AsyncCobottaStateClient(config=Config, logger=logger)
    client = AsyncCobottaClient(config=Config, logger=logger)

    # await client.reset_error()

    # speed の入手などには take_arm が必要(アームごとのパラメータなので)
    logger.info("take_arm")
    ret = await client.take_arm()

    logger.info("turn_on_motor")
    await client.turn_on_motor()

    logger.info(f"motion_mode = {MotionMode.PTP}")
    client.motion_mode = MotionMode.PTP

    ret = await client.get_P(f"P110")
    logger.info(f"== get_P(): {ret})")

    ret = await client.move("P110")
    # ret = await client.move(f"@E {num}+(-12,-22,0)", bstrOpt=30)
    # await client.wait_for_complete()

    # assert ret is not None, "接続失敗"

    # current_pos = await client.get_current_pos()
    # logger.info(f"current_position: {current_pos}")
    assert "result" == "result"
