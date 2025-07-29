#!/usr/bin/env python
"""
Kengo NAKADA:
https://github.com/shimane-dev, https://github.com/kengo-nakada
kengo.nakada@mat.shimane-u.ac.jp, kengo.nakada@gmail.com
"""
from cobotta2.config import Config
from cobotta2.cobotta_ctrl import CobottaCtrl
from cobotta2.server_fastapi.routers import CobottaRouterCtrl
from cobotta2.server_fastapi.spec_ctrl import cobotta_ctrl_api_spec

from fastapi_frame.api_server import FastApiServer
from x_logger.x_logger import XLogger


def server_start():
    Config.load_yaml("../config_server1.yaml")
    logger = XLogger(
        log_level="debug",
        logger_name=Config.COBOTTA_SERVER_LOGGER_NAME,
        log_mode="rotate",
        log_name="c:/logs/cobotta_server.log",
    )

    logger.info(f"COBOTTA IP = {Config.COBOTTA_IP}")
    logger.info(f"SERVER IP = {Config.SERVER_IP}")
    logger.info(f"SERVER PORT = {Config.SERVER_PORT}")

    server = FastApiServer(
        device_cls=CobottaCtrl,  # 制御クラス
        router_cls=CobottaRouterCtrl,  # routerクラス
        config=Config,
        api_spec=cobotta_ctrl_api_spec,
        device_kwargs={
            "cobotta_ip": Config.COBOTTA_IP
        },  # COBOTTA制御Classのコンストラクタ引数)
        logger=logger,
        logger_name=Config.COBOTTA_SERVER_LOGGER_NAME,  # LOGGER_NAME
        lifespan_msg_prefix="COBOTTA",
    )
    server.run(host=Config.SERVER_IP, port=Config.SERVER_PORT)


if __name__ == "__main__":
    server_start()
