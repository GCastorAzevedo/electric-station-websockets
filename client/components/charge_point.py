import asyncio
import logging
from datetime import datetime
from typing import List

from ocpp.v201 import ChargePoint as cp
from ocpp.v201 import call
from ocpp.v201.enums import ConnectorStatusType, RegistrationStatusType
from websockets.client import WebSocketClientProtocol

logging.basicConfig(level=logging.INFO)


class ChargePoint(cp):
    _connectors: List[int]

    def __init__(
        self,
        id: str,
        connection: WebSocketClientProtocol,
        response_timeout: int = 30,
        connectors: List[int] = [],
    ):
        super().__init__(id, connection, response_timeout)
        self._connectors = connectors

    # TODO: change to a descriptive name like send_b01_cold_boot_charging_system
    async def send_b01_cold_boot_charging_system_notification(self) -> None:
        """
        Implements B01 - Cold Boot Charging Station
        """
        request = call.BootNotificationPayload(
            charging_station={"model": "Wallbox XYZ", "vendor_name": "anewone"},
            reason="PowerUp",
        )
        response = await self.call(request)

        if response.status == RegistrationStatusType.accepted:
            logging.info("Connected to central system.")
            for id in self._connectors:
                await self.send_status_notification(
                    id, 0, ConnectorStatusType.unavailable
                )
                await self.reboot_connector(id)
                await self.send_status_notification(
                    id, 0, ConnectorStatusType.available
                )
            await self.send_heartbeat(response.interval)
        elif response.status == RegistrationStatusType.rejected:
            await asyncio.sleep(10)
            await self.send_b03_cold_boot_charging_station_rejected_notification()
        elif response.status == RegistrationStatusType.pending:
            await asyncio.sleep(10)
            await self.send_b02_cold_boot_charging_station_pending_notification()

    async def send_b02_cold_boot_charging_station_pending_notification(self) -> None:
        """
        Implements B02 - Cold Boot Charging Station - Pending
        """
        pass

    async def send_b03_cold_boot_charging_station_rejected_notification(self) -> None:
        """
        Implements B03 - Cold Boot Charging Station - Rejected
        """
        pass

    async def reboot_connector(self, connector_id: int = 0) -> None:
        logging.info(f"Rebooted connector {connector_id}")
        pass

    async def send_status_notification(
        self,
        connector_id: int,
        evse_id: int,
        status: ConnectorStatusType = ConnectorStatusType.available,
    ) -> None:
        request = call.StatusNotificationPayload(
            timestamp=datetime.utcnow().isoformat(),
            connector_status=status,
            evse_id=evse_id,
            connector_id=connector_id,
        )
        response = await self.call(request)
        logging.info(response)

    async def send_heartbeat(self, interval: int) -> None:
        request = call.HeartbeatPayload()
        while True:
            await self.call(request)
            await asyncio.sleep(interval)
