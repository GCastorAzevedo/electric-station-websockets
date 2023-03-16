import asyncio
import logging

import websockets.server
from auth.credentials import check_credentials
from config import HOST, PORT, SERVER_NAME, SUB_PROTOCOL
from csms.handlers import on_connect

logging.basicConfig(level=logging.INFO)


async def main() -> None:
    server = await websockets.server.serve(
        on_connect,
        HOST,
        PORT,
        subprotocols=[SUB_PROTOCOL],
        create_protocol=websockets.basic_auth_protocol_factory(
            realm=SERVER_NAME, check_credentials=check_credentials
        ),
    )
    logging.info("WebSocket Server Started")
    await server.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())
