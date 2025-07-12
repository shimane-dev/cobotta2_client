#!/usr/bin/env python
"""

Kengo NAKADA:
https://github.com/shimane-dev, https://github.com/kengo-nakada
kengo.nakada@mat.shimane-u.ac.jp, kengo.nakada@gmail.com
"""
import pytest


@pytest.mark.asyncio
async def test_fastapi_Async_test_1_2():
    import logging

    # httpx のログを WARNING レベル以上にする（INFO を抑制）
    logging.getLogger("httpx").setLevel(logging.WARNING)

    from cobotta2.config import Config
    from cobotta2.server_fastapi.clients import AsyncCobottaClient
    from cobotta2.server_fastapi.models.motion import MotionMode
    from x_logger.x_logger import XLogger

    Config.load_yaml("config_server1.yaml")

    _logger = XLogger(log_level="info", logger_name=Config.COBOTTA_CLIENT_LOGGER_NAME)
    client = AsyncCobottaClient(config=Config, logger=_logger)

    try:
        _logger.info("== take arm()")
        await client.take_arm()

        _logger.info("== turn on motor()")
        await client.turn_on_motor()

        while True:
            _logger.info("== run test()")
            await client.test()
            await client.wait_for_complete()

            _logger.info("== run test2()")
            await client.test2()
            await client.wait_for_complete()

        # time.sleep(0.1)
    except KeyboardInterrupt:
        _logger.info("KeyboardInterrupt")
    except Exception as e:
        _logger.error(e)
    finally:
        assert "result" == "result"
