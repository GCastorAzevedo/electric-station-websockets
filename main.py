# import asyncio
# from typing import Any

# import websockets.server
# from websockets.typing import Subprotocol

# HOST: str = "0.0.0.0"
# PORT: int = 9000
# SUB_PROTOCOL: Subprotocol = Subprotocol("ocpp2.0.1")


# async def on_connect(websocket: Any, path: str) -> None:
#     await websocket.send("Connection made succesfully.")
#     print(f"Charge point {path} connected")


# async def main() -> None:
#     server = await websockets.server.serve(
#         on_connect, HOST, PORT, subprotocols=[SUB_PROTOCOL]
#     )
#     await server.wait_closed()


# if __name__ == "__main__":
#     asyncio.run(main())
#     # python -m websockets ws://localhost:9000/test_charge_point
