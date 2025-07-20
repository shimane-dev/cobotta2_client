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

    import time
    from cobotta2.config import Config
    from cobotta2.server_fastapi.clients import AsyncCobottaClient
    from cobotta2.server_fastapi.models.motion import MotionMode
    from x_logger.x_logger import XLogger

    Config.load_yaml("config_server1.yaml")

    logger = XLogger(log_level="info", logger_name=Config.COBOTTA_CLIENT_LOGGER_NAME)
    client = AsyncCobottaClient(config=Config, logger=logger)

    await client.take_arm()
    ret = await client.turn_on_motor()
    assert ret is not None, "接続失敗"

    logger.info("== run speed()")
    speed = await client.get_speed()
    jspeed = await client.get_jspeed()
    extspeed = await client.get_extspeed()
    logger.info(f"speed={speed}, extspeed={extspeed}, jspeed={jspeed},")

    # assert "result" == "result"
    # send_command("unknown")  # これはエラーになる


if __name__ == "__main__":
    asyncio.run(main())
