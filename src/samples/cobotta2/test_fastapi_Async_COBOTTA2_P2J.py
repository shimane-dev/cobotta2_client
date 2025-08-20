#!/usr/bin/env python
"""
内部変数値を読んで、それを配列に入れなおして、そこに移動する

Kengo NAKADA:
https://github.com/shimane-dev, https://github.com/kengo-nakada
kengo.nakada@mat.shimane-u.ac.jp, kengo.nakada@gmail.com
"""
import pytest


@pytest.mark.asyncio
async def test_fastapi_Async_test_1_2():
    import logging
    import asyncio
    import json
    from pathlib import Path

    # httpx のログを WARNING レベル以上にする（INFO を抑制）
    logging.getLogger("httpx").setLevel(logging.WARNING)

    from cobotta2 import Config, MotionMode
    from cobotta2.server import AsyncCobottaClient
    from x_logger import XLogger

    HERE = Path(__file__).parent
    Config.load_yaml(HERE / "config_cobotta2.yaml")
    # Config.load_yaml("config_cobotta2.yaml")

    logger = XLogger(log_level="info", logger_name=Config.CLIENT_LOGGER_NAME)
    client = AsyncCobottaClient(config=Config, logger=logger)
    # await client.reset_error()
    # await client.release_arm()

    # await client.turn_on_motor()
    # await client.take_arm()

    P110_camera = (
        197.74189325511722,  # X
        -102.87065719423421,  # y
        # 45.40395449388056,  # z
        180.0,  # z
        -176.46837944742447,  # rx
        # 10.232977777915506,  # ry
        0.0,
        176.76296478619867,  # rz
        261.0,
    )
    ret_j = await client.p2j(P110_camera)
    logger.info(json.dumps(ret_j, indent=2))

    ret_p = await client.j2p(ret_j)
    logger.info(json.dumps(ret_p, indent=2))

    assert True


#   logger.info("---------- カメラで画像認識 -------------------")
#   # name = "EVP2"
#   name = "EVP2_02"
#   # name = "P_P62"
#   await client.take_script(name)
#   await client.run_script()
#   logger.info(f"Result: {client.P10}")
#   await client.wait_for_complete()

#   logger.info("----------- 画像認識のセンターへmove  --------------")
#   await client.take_arm()
#   # client.move("P10+(0,0,-5)", speed=30)
#   await client.move("P10", offset=(0, 0, -13), speed=30)
#   await client.wait_for_complete()

#   logger.info("----------- 指先を９０度回転  --------------")
#   # client.drive_EX((6, -90))  # 相対
#   await client.rotate_H(-90.0)  # 相対
#   await client.wait_for_complete()

#   logger.info("----------- 近づく(offset-move)  --------------")
#   pos = await client.get_current_position()

#   ############### 基本動作テスト
#   # client.cored_type = "P"
#   # client.path_blend = "@P"
#   # client.motion_mode = MotionMode.PTP
#   # # client.bstr_opt = "Speed=100,Next"
#   # client.move(pos)
#   ##########################

#   ### offset 付きの基本動作
#   # await client.move(pos, offset=(0, 0, -13), speed=30)

#   # # client.hand_move_A(30, speed=100)  # full-open
#   # client.wait_for_complete()

#   # ここで、P10 を入れると J6 の値が元に戻るので 直前の回転が意味がなくなる
#   # client.move("P10", offset=(0, 0, -15), speed=30)

#   assert "result" == "result"

#   # except KeyboardInterrupt as e:
#   #     logger.error(e)
#   # finally:
#   #     await client.disconnect()


# def test_local_reset_error():
#     p = multiprocessing.Process(target=worker)
#     p.start()
#     # p.terminate()
#     p.join()  # join()なしでもkillはされる
