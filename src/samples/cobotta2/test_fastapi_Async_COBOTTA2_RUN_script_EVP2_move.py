#!/usr/bin/env python
"""
内部変数値を読んで、それを配列に入れなおして、そこに移動する

Kengo NAKADA:
https://github.com/shimane-dev, https://github.com/kengo-nakada
kengo.nakada@mat.shimane-u.ac.jp, kengo.nakada@gmail.com
"""
import pytest
import asyncio


@pytest.mark.asyncio
async def test_fastapi_Async_test_1_2():
    import logging

    # httpx のログを WARNING レベル以上にする（INFO を抑制）
    logging.getLogger("httpx").setLevel(logging.WARNING)

    import time
    from cobotta2.config import Config
    from cobotta2.server_fastapi.clients import AsyncCobottaClient
    from x_logger.x_logger import XLogger

    Config.load_yaml("config_server2.yaml")

    logger = XLogger(log_level="info", logger_name=Config.CLIENT_LOGGER_NAME)
    client = AsyncCobottaClient(config=Config, logger=logger)
    await client.reset_error()
    await client.release_arm()

    await client.turn_on_motor()

    logger.info("--------- カメラポジションへ -----------------")
    await client.take_arm()
    await client.open_hand()

    # await client.move("P110", speed=100)
    # based on P110
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
    ret = await client.move(P110_camera, speed=100)
    ret = await client.reset_error()
    if ret is None or ret is False:
        assert False, "Connect Error"

    logger.info("---------- Hand 初期位置移動 -------------------")
    await client.init_hand()
    await asyncio.sleep(1)
    await client.release_arm()

    logger.info("---------- カメラで画像認識 -------------------")
    # name = "EVP2"
    name = "EVP2_02"
    # name = "P_P62"
    await client.take_script(name)
    await client.run_script()
    logger.info(f"Result: {client.P10}")
    await client.wait_for_complete()

    logger.info("----------- 画像認識のセンターへmove  --------------")
    await client.take_arm()
    # client.move("P10+(0,0,-5)", speed=30)
    await client.move("P10", offset=(0, 0, -13), speed=30)
    await client.wait_for_complete()

    logger.info("----------- 指先を９０度回転  --------------")
    ret = await client.drive_EX((6, -90))  # 相対
    # await client.rotate_H(-90.0)  # 相対
    if not ret or ret is None:
        # 開始状態によっては指の回転状態が異なるので -90 でエラーとなることがあるのでそのときは +90 でチャレンジ
        await client.reset_error()
        await client.release_arm()
        await client.take_arm()
        ret2 = await client.drive_EX((6, 90))  # 相対
        if not ret2 or ret2 is None:
            sys.exit(-1)

    await client.wait_for_complete()

    logger.info("----------- 近づく(offset-move)  --------------")
    pos = client.get_current_position()
    # offset 付きの基本動作
    # ret = client.move(pos, path_blend="@0", offset=(0, 0, -25), speed=30)
    ret = client.move(pos, path_blend="@E", offset=(0, 0, -25), speed=30)
    if not ret:
        sys.exit(-1)  ## ここでぶつかる恐れがある

    ############### 基本動作テスト
    # client.cored_type = "P"
    # client.path_blend = "@P"
    # client.motion_mode = MotionMode.PTP
    # # client.bstr_opt = "Speed=100,Next"
    # client.move(pos)
    ##########################

    ### offset 付きの基本動作
    # await client.move(pos, offset=(0, 0, -13), speed=30)

    # # client.hand_move_A(30, speed=100)  # full-open
    # client.wait_for_complete()

    # ここで、P10 を入れると J6 の値が元に戻るので 直前の回転が意味がなくなる
    # client.move("P10", offset=(0, 0, -15), speed=30)

    assert "result" == "result"

    # except KeyboardInterrupt as e:
    #     logger.error(e)
    # finally:
    #     await client.disconnect()


# def test_local_reset_error():
#     p = multiprocessing.Process(target=worker)
#     p.start()
#     # p.terminate()
#     p.join()  # join()なしでもkillはされる
