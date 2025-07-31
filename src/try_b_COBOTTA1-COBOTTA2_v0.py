#!/usr/bin/env python
"""
cobotta1/cobotta2 の平行（同時）動作のサンプル

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

from cobotta2 import Config, MotionMode
from cobotta2.server import AsyncCobottaClient
from x_logger import XLogger


# @pytest.mark.asyncio
async def main():
    logger = XLogger(log_level="info", logger_name=Config.CLIENT_LOGGER_NAME)
    t1 = asyncio.create_task(c1(logger))
    t2 = asyncio.create_task(c2(logger))
    # await asyncio.gather(t2)
    await asyncio.gather(t1, t2)


async def c1(
    logger: XLogger = None,
):
    Config.load_yaml("config_cobotta1.yaml")
    client1 = AsyncCobottaClient(config=Config, logger=logger)
    await client1.reset_error()
    pass


async def c2(
    logger: XLogger = None,
):
    """"""
    Config.load_yaml("config_cobotta2.yaml")
    client2 = AsyncCobottaClient(config=Config, logger=logger)
    await client2.reset_error()

    try:
        ret = await client2.take_arm()
        if ret is None or ret is False:
            sys.exit(-1)
        await client2.turn_on_motor()

        # await client.set_speed(100)

        # move Target
        client2.motion_mode = MotionMode.PTP
        await client2.move("P110", speed=50)

        client2.motion_mode = MotionMode.LINE
        await client2.move("P110", speed=60)
        await client2.move("P111", speed=60)
        await client2.move("P112", speed=60)
        await client2.move("P113", speed=60)
        await client2.move("P114", speed=60)
        await client2.move("P115", speed=60)
        await client2.move("P116", speed=60)
        await client2.move("P117", speed=60)
        await client2.open_hand()
        await client2.wait_for_complete()

        await client2.move("P116", speed=60)
        await client2.move("P115", speed=60)
        await client2.move("P114", speed=60)
        await client2.move("P113", speed=60)
        await client2.move("P112", speed=60)
        await client2.move("P111", speed=60)
        await client2.move("P110", speed=60)
        await client2.wait_for_complete()

        # # cobotta.move("P3", bstrOpt=100)  # home
        # cobotta.motion_mode = MotionMode.LINE
        # cobotta.move("@E P62+(0,0,5)", bstrOpt=100)
        # cobotta.wait_for_complete()
        # current_pos = cobotta.get_current_pos()
        # logger.info(f"current_position: {current_pos}")

    except Exception as e:
        logger.error(f"error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
