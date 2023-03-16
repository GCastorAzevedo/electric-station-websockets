import asyncio
import logging

import websockets.server
from config import HOST, PORT, SERVER_NAME, SUB_PROTOCOL
from csms.handlers import on_connect

logging.basicConfig(level=logging.INFO)


async def main() -> None:
    server = await websockets.server.serve(
        on_connect, HOST, PORT, subprotocols=[SUB_PROTOCOL]
    )
    logging.info("WebSocket Server Started")
    await server.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())
