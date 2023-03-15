import asyncio
import logging

import websockets.client
from components.charge_point import ChargePoint
from websockets.typing import Subprotocol

logging.basicConfig(level=logging.INFO)

HOST: str = "0.0.0.0"
PORT: int = 9000
SUB_PROTOCOL: Subprotocol = Subprotocol("ocpp2.0.1")


# async def main() -> None:
#     charge_point_name: str = "charge_point_1"
#     endpoint: str = f"ws://{HOST}:{PORT}/{charge_point_name}"
#     async with websockets.client.connect(endpoint, subprotocols=[SUB_PROTOCOL]) as ws:
#         cp = ChargePoint(charge_point_name, ws, connectors=[1])

#         await asyncio.gather(
#             cp.start(), cp.send_b01_cold_boot_charging_system_notification()
#         )


# if __name__ == "__main__":
#     asyncio.run(main())


async def main():
    async with websockets.connect(
        "ws://localhost:9000/CP_1", subprotocols=["ocpp2.0.1"]
    ) as ws:
        cp = ChargePoint("CP_1", ws, connectors=[1])

        await asyncio.gather(
            cp.start(), cp.send_b01_cold_boot_charging_system_notification()
        )
        # cp.send_boot_notification())


if __name__ == "__main__":
    asyncio.run(main())
