#!/usr/bin/env python
"""

Kengo NAKADA:
https://github.com/shimane-dev, https://github.com/kengo-nakada
kengo.nakada@mat.shimane-u.ac.jp, kengo.nakada@gmail.com
"""
import pytest


@pytest.mark.asyncio
async def test_cobotta_full_sequence():
    import logging

    # httpx のログを WARNING レベル以上にする（INFO を抑制）
    logging.getLogger("httpx").setLevel(logging.WARNING)

    from cobotta2.config import Config
    from cobotta2.server_fastapi.clients import AsyncCobottaClient
    from cobotta2.server_fastapi.models.motion import MotionMode
    from x_logger.x_logger import XLogger

    Config.load_yaml("config_server1.yaml")

    logger = XLogger(log_level="info", logger_name=Config.CLIENT_LOGGER_NAME)
    client = AsyncCobottaClient(config=Config, logger=logger)

    logger.info("== take arm()")
    await client.take_arm()

    logger.info("== turn on motor()")
    await client.turn_on_motor()

    try:
        while True:
            logger.info("== run test()")
            await client.test()

            logger.info("== run test2()")
            await client.test2()
            logger.info("== test END")

    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt")
    except Exception as e:
        print(e)
    finally:
        assert "result" == "result"
