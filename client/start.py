import asyncio
import logging

import websockets.client
from components.charge_point import ChargePoint, discover_charge_point_name
from components.connectors import discover_connectors
from config import HOST, PASSWORD, PORT, SUB_PROTOCOL, USER

logging.basicConfig(level=logging.INFO)


async def main() -> None:
    charge_point_name = discover_charge_point_name()
    connectors = discover_connectors(charge_point_name)
    async with websockets.client.connect(
        f"ws://{HOST}:{PORT}/{charge_point_name}", subprotocols=[SUB_PROTOCOL]
    ) as ws:
        cp = ChargePoint(charge_point_name, ws, connectors=connectors)

        await asyncio.gather(
            cp.start(), cp.send_b01_cold_boot_charging_system_notification()
        )


if __name__ == "__main__":
    asyncio.run(main())
