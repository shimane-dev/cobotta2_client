#!/usr/bin/env python
"""
Kengo NAKADA:
https://github.com/shimane-dev, https://github.com/kengo-nakada
kengo.nakada@mat.shimane-u.ac.jp, kengo.nakada@gmail.com
"""
# import pytest
import asyncio


# @pytest.mark.asyncio
async def main():
    import logging

    # httpx のログを WARNING レベル以上にする（INFO を抑制）
    logging.getLogger("httpx").setLevel(logging.WARNING)

    from cobotta2.config import Config
    from cobotta2.server_fastapi.clients import AsyncCobottaClient
    from cobotta2.server_fastapi.models.motion import MotionMode
    from x_logger.x_logger import XLogger

    Config.load_yaml("../config_server1.yaml")

    logger = XLogger(log_level="info", logger_name=Config.COBOTTA_CLIENT_LOGGER_NAME)
    client = AsyncCobottaClient(config=Config, logger=logger)
    await client.reset_error()

    # speed の入手などには take_arm が必要(アームごとのパラメータなので)
    ret = await client.take_arm()
    assert ret is not None, "接続失敗"

    ret = await client.turn_on_motor()
    assert ret is not None, "接続失敗"

    await client.hand_move_A(30, 100)

    assert ret is not None, "接続失敗"
    await client.wait_for_complete()

    # current_pos = await client.get_current_pos()
    # _logger.info(f"current_position: {current_pos}")


if __name__ == "__main__":
    asyncio.run(main())
