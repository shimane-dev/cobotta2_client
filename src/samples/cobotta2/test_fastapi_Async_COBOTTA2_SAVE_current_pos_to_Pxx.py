#!/usr/bin/env python
"""

Kengo NAKADA:
https://github.com/shimane-dev, https://github.com/kengo-nakada
kengo.nakada@mat.shimane-u.ac.jp, kengo.nakada@gmail.com
"""
import pytest


@pytest.mark.asyncio
async def test_fastapi_state():
    import logging

    # httpx のログを WARNING レベル以上にする（INFO を抑制）
    logging.getLogger("httpx").setLevel(logging.WARNING)

    import time
    from cobotta2.config import Config
    from cobotta2.server_fastapi.clients import AsyncCobottaClient
    from cobotta2.server_fastapi.models.motion import MotionMode
    from x_logger.x_logger import XLogger

    Config.load_yaml("config_server2.yaml")

    print(f"SERVER IP:{Config.SERVER_IP}")
    print(f"SERVER PORT:{Config.SERVER_PORT}")

    Config.load_yaml("config_server2.yaml")

    logger = XLogger(log_level="info", logger_name=Config.CLIENT_LOGGER_NAME)
    client = AsyncCobottaClient(config=Config, logger=logger)
    ret = await client.reset_error()
    if ret is None or ret is False:
        assert False, "Connect Error"

    try:
        # busy_status などの問い合わせは take arm しないほうがいい。
        current_pos = await client.get_current_position()
        logger.info(current_pos)
        logger.info(current_pos[:6])

        # current_pos を Pxx に書き込む
        num = 45
        await client.set_P(num, current_pos[:6])

    except Exception as e:
        print(e)
    assert "result" == "result"
    # send_command("unknown")  # これはエラーになる
