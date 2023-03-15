import asyncio
import logging

import websockets.server
from csms.handlers import on_connect
from websockets.typing import Subprotocol

logging.basicConfig(level=logging.INFO)

HOST: str = "0.0.0.0"
PORT: int = 9000
SUB_PROTOCOL: Subprotocol = Subprotocol("ocpp2.0.1")


async def main() -> None:
    server = await websockets.server.serve(
        on_connect, HOST, PORT, subprotocols=[SUB_PROTOCOL]
    )
    logging.info("WebSocket Server Started")
    await server.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())
