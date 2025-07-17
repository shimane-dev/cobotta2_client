#!/usr/bin/env python
"""
Kengo NAKADA:
https://github.com/shimane-dev, https://github.com/kengo-nakada
kengo.nakada@mat.shimane-u.ac.jp, kengo.nakada@gmail.com
"""
from cobotta2.config import Config
from cobotta2.cobotta_ctrl_state import CobottaState
from cobotta2.server_fastapi.routers import CobottaRouterState
from cobotta2.server_fastapi.spec_state import cobotta_state_api_spec

from fastapi_frame.api_server import FastApiServer
from x_logger.x_logger import XLogger


if __name__ == "__main__":
    Config.load_yaml("config_server2_state.yaml")
    logger = XLogger(log_level="debug", logger_name=Config.COBOTTA_SERVER_LOGGER_NAME)

    logger.info(f"COBOTTA IP = {Config.COBOTTA_IP}")
    logger.info(f"SERVER IP = {Config.SERVER_IP}")
    logger.info(f"SERVER PORT = {Config.SERVER_PORT}")

    server = FastApiServer(
        device_cls=CobottaState,  # 制御クラス
        router_cls=CobottaRouterState,  # 継承でつくった router
        config=Config,
        api_spec=cobotta_state_api_spec,
        device_kwargs={
            "cobotta_ip": Config.COBOTTA_IP
        },  # COBOTTA制御Classのコンストラクタ引数)
        logger=logger,
        logger_name=Config.COBOTTA_SERVER_LOGGER_NAME,
        lifespan_msg_prefix="COBOTTA",
    )
    server.run(host=Config.SERVER_IP, port=Config.SERVER_PORT)
