#!/usr/bin/env python
"""
try_a_v02.py (version 0.0.4)

frame 0.3.0
cobotta 0.5.5

Kengo NAKADA:
https://github.com/shimane-dev, https://github.com/kengo-nakada
kengo.nakada@mat.shimane-u.ac.jp, kengo.nakada@gmail.com
"""
# import pytest
import sys
import asyncio
import multiprocessing

import logging

# httpx のログを WARNING レベル以上にする（INFO を抑制）
logging.getLogger("httpx").setLevel(logging.WARNING)

from cobotta2.config import Config
from cobotta2.server_fastapi.clients import AsyncCobottaClient
from cobotta2.server_fastapi.models.motion import MotionMode
from x_logger import XLogger


async def main():
    """"""
    Config.load_yaml("config_server1.yaml")

    logger = XLogger(log_level="info", logger_name=Config.COBOTTA_CLIENT_LOGGER_NAME)
    client = AsyncCobottaClient(config=Config, logger=logger)
    await client.reset_error()

    try:
        # speed の入手などには take_arm が必要(アームごとのパラメータなので)
        ret = await client.take_arm()
        if ret is None or ret is False:
            logger.error("connect failed.")
            sys.exit(-1)
        await client.turn_on_motor()

        # await client.set_speed(100)

        current_pos = await client.get_current_pos()
        logger.info(f"current_position: {current_pos}")
        P120 = (
            30.469897335318052,
            428.5388768411265,
            176.98776161519538,
            173.14641997469639,
            71.16606465468504,
            -95.40025814412292,
            261.0,
        )

        await client.move(P120, path_blend="@E")
        await client.wait_for_complete()

        # cobotta.move("P121", path_blend="@E")

        current_pos = await client.get_current_pos()
        logger.info(f"current_position: {current_pos}")
        P121 = (
            44.66388605419964,
            304.0272038932793,
            273.7832327046305,
            172.18749247890455,
            21.886399479886972,
            -95.8109958415797,
            261.0,
        )
        await client.move(P121, path_blend="@E")
        await client.wait_for_complete()

    except Exception as e:
        logger.error(f"error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
