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

    from cobotta2 import Config
    from cobotta2.server import AsyncCobottaClient
    from x_logger import XLogger

    HERE = Path(__file__).parent
    Config.load_yaml(HERE / "config_cobotta1.yaml")
    # Config.load_yaml("config_cobotta1.yaml")

    logger = XLogger(log_level="info", logger_name=Config.CLIENT_LOGGER_NAME)
    client = AsyncCobottaClient(config=Config, logger=logger)
    assert client is not None, "Connect Error"

    # while True:
    # busy_status などの問い合わせは take arm しないほうがいい。
    result = await client.busy_status()
    # result = await client.state("state")
    logger.info(f"busy_status() = {result}")
    assert "result" == "result"
    # send_command("unknown")  # これはエラーになる
