#!/usr/bin/env python
"""
内部変数値を読んで、それを配列に入れなおして、そこに移動する

Kengo NAKADA:
https://github.com/shimane-dev, https://github.com/kengo-nakada
kengo.nakada@mat.shimane-u.ac.jp, kengo.nakada@gmail.com
"""
import pytest


@pytest.mark.asyncio
async def test_fastapi_Async_move1_P2():
    import logging

    # httpx のログを WARNING レベル以上にする（INFO を抑制）
    logging.getLogger("httpx").setLevel(logging.WARNING)

    from cobotta2.config import Config
    from cobotta2.server_fastapi.clients import AsyncCobottaClient
    from cobotta2.server_fastapi.models.motion import MotionMode
    from x_logger.x_logger import XLogger

    Config.load_yaml("../config_server1.yaml")

    logger = XLogger(log_level="info", logger_name=Config.CLIENT_LOGGER_NAME)
    client = AsyncCobottaClient(config=Config, logger=logger)
    await client.reset_error()

    # speed の入手などには take_arm が必要(アームごとのパラメータなので)
    ret = await client.take_arm()
    assert ret is not None, "接続失敗"

    ret = await client.turn_on_motor()
    assert ret is not None, "接続失敗"

    client.motion_mode = MotionMode.PTP
    pos = (
        -29.0453511306835,
        343.1440808456958,
        115.31284305934872,
        -178.28955954148657,
        -16.619847808793967,
        141.1028536689876,
    )

    ###########################################
    client.motion_mode = MotionMode.PTP
    await client.set_cored_type("P")
    ret = await client.move(pos)
    ###########################################

    assert ret is not None, "接続失敗"
    await client.wait_for_complete()

    current_pos = client.get_current_position()
    logger.info(f"current_position: {current_pos}")
    assert "result" == "result"
