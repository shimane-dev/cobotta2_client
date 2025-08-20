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
    import asyncio
    from pathlib import Path

    # httpx のログを WARNING レベル以上にする（INFO を抑制）
    logging.getLogger("httpx").setLevel(logging.WARNING)

    from cobotta2 import Config, MotionMode
    from cobotta2.server import AsyncCobottaClient
    from x_logger import XLogger

    HERE = Path(__file__).parent
    Config.load_yaml(HERE / "config_cobotta2.yaml")
    # Config.load_yaml("config_cobotta2.yaml")

    print(f"SERVER IP:{Config.SERVER_IP}")
    print(f"SERVER PORT:{Config.SERVER_PORT}")

    logger = XLogger(log_level="info", logger_name=Config.CLIENT_LOGGER_NAME)
    client = AsyncCobottaClient(config=Config, logger=logger)

    ret = await client.reset_error()
    if ret is None or ret is False:
        assert False, "Connect Error"

    try:
        # busy_status などの問い合わせは take arm しないほうがいい。
        ret = await client.rotate(30, speed=50)
    except Exception as e:
        print(e)
    assert "result" == "result"
    # send_command("unknown")  # これはエラーになる
