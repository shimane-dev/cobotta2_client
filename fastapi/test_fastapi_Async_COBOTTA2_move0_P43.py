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

    # httpx のログを WARNING レベル以上にする（INFO を抑制）
    logging.getLogger("httpx").setLevel(logging.WARNING)

    from cobotta2.config import Config
    from cobotta2.server_fastapi.clients import AsyncCobottaClient
    from cobotta2.server_fastapi.models.motion import MotionMode
    from x_logger.x_logger import XLogger

    Config.load_yaml("config_server2.yaml")

    _logger = XLogger(log_level="info", logger_name=Config.COBOTTA_CLIENT_LOGGER_NAME)
    client = AsyncCobottaClient(config=Config, logger=_logger)

    # await client.reset_error()

    # speed の入手などには take_arm が必要(アームごとのパラメータなので)
    _logger.info("take_arm")
    ret = await client.take_arm()
    assert ret is not None, "接続失敗"

    _logger.info("turn_on_motor")
    ret = await client.turn_on_motor()
    assert ret is not None, "接続失敗"

    _logger.info(f"motion_mode = {MotionMode.PTP}")
    client.motion_mode = MotionMode.PTP

    num = "P43"
    _logger.info(f"{num}")
    ret = await client.get_P(f"{num}")
    _logger.info(f"{num}: {ret}")

    _logger.info(f"move({num})")
    ret = await client.move(f"{num}", bstrOpt=50)
    await client.wait_for_complete()

    current_pos = await client.get_current_pos()
    _logger.info(f"current_position: {current_pos}")
    assert "result" == "result"
