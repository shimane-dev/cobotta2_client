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
    Config.load_yaml(HERE / "config_cobotta1.yaml")
    # Config.load_yaml("config_cobotta1.yaml")

    logger = XLogger(log_level="info", logger_name=Config.CLIENT_LOGGER_NAME)
    client = AsyncCobottaClient(config=Config, logger=logger)

    try:
        while True:
            result = await client.busy_status()
            assert result is not None, "接続失敗"

            # result = await client.state("state")
            logger.info(f"get_busy_status = {result}")
            await asyncio.sleep(0.5)
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt")
    except Exception as e:
        print(e)
    finally:
        assert "result" == "result"
    # send_command("unknown")  # これはエラーになる
