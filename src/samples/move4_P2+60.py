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

    Config.load_yaml("config_server1.yaml")

    logger = XLogger(log_level="info", logger_name=Config.COBOTTA_CLIENT_LOGGER_NAME)
    client = AsyncCobottaClient(config=Config, logger=logger)
    await client.reset_error()

    # ########################
    # take_arm
    # speed の入手などには take_arm が必要(アームごとのパラメータなので)
    ret = await client.take_arm()
    assert ret is not None, "接続失敗"

    # ########################
    # turn_on_motor
    ret = await client.turn_on_motor()
    assert ret is not None, "接続失敗"

    # ########################
    # Current_position
    current_pos = await client.get_current_pos()
    logger.info(f"current_pos = {current_pos}")

    # # P2 <--PTP--> P3
    name = "P62"

    # # ########################
    # # Target_position
    # name_pos = await client.get_P(2)
    # target = dict(name_pos)["result"][:6]

    # _logger.info(f"name_pos: {name_pos}")
    # _logger.info(f"type(name_pos): {type(name_pos)}")
    # _logger.info(f'dict(name_pos)["result"][:6]: {target}')
    # print(target)
    # print(type(target))

    pos = (
        115.07630157470703,
        -272.94757080078125,
        240.98133850097656,
        171.91989135742188,
        -21.261798858642578,
        -19.010150909423828,
    )
    logger.info(f"pos: {pos}")

    # ########################
    # move Target
    client.cored_type = "P"
    client.pose_format = "@P"
    client.motion_mode = MotionMode.PTP
    # cobotta.bstr_opt = "Speed=100,Next"
    await client.move(pos)

    # ########################
    # move Target
    # cobotta.wait_for_complete()

    # # ########################
    # # move Target
    # cobotta.motion_mode = MotionMode.PTP
    # ret = await cobotta.move("P2", bstrOpt=100)
    # assert ret is not None, "接続失敗"
    # await cobotta.wait_for_complete()

    # current_pos = cobotta.get_current_pos()
    # _logger.info(f"current_position: {current_pos}")
    assert "result" == "result"
