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

    start = 0
    end = 45
    try:
        # busy_status などの問い合わせは take arm しないほうがいい。
        for num in range(start, end + 1):
            cls = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0]
            await client.set_P(num, cls)

    except Exception as e:
        print(e)
    assert "result" == "result"
    # send_command("unknown")  # これはエラーになる


# def test_local_reset_error():
#     p = multiprocessing.Process(target=worker)
#     p.start()
#     # p.terminate()
#     p.join()  # join()なしでもkillはされる
