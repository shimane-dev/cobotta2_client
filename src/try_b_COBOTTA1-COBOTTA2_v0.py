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

# from cobotta2 import Config, MotionMode
# from cobotta2.server import AsyncCobottaClient

from try_a_COBOTTA1_v03 import worker_cobotta1
from try_a_COBOTTA2_v02 import worker_cobotta2

from x_logger import XLogger


# @pytest.mark.asyncio
async def main():
    # logger = XLogger(log_level="info", logger_name=Config.CLIENT_LOGGER_NAME)
    # t1 = asyncio.create_task(c1(logger))
    # t2 = asyncio.create_task(c2(logger))
    t1 = asyncio.create_task(worker_cobotta1())
    t2 = asyncio.create_task(worker_cobotta2())
    # await asyncio.gather(t2)
    await asyncio.gather(t1, t2)


if __name__ == "__main__":
    asyncio.run(main())
