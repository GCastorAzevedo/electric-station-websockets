import logging
from datetime import datetime
from typing import Dict
from urllib.parse import unquote

from ocpp.routing import on
from ocpp.v201 import ChargePoint as cp
from ocpp.v201.call_result import (
    BootNotificationPayload,
    HeartbeatPayload,
    StatusNotificationPayload,
)
from ocpp.v201.enums import Action, RegistrationStatusType
from websockets.server import WebSocketServerProtocol

logging.basicConfig(level=logging.INFO)


# TODO: as functionalities grow, break central.py into modules.
class ChargePoint(cp):
    """
    Implements Server-side representation of a charge point
    for a subset of OCPP-compliant actions.
    """

    @on(Action.BootNotification)
    async def on_boot_notification(
        self, charging_station: Dict, reason: str
    ) -> BootNotificationPayload:
        logging.debug(f"{charging_station=} {reason=}")
        return BootNotificationPayload(
            current_time=datetime.utcnow().isoformat(),
            interval=10,
            status=RegistrationStatusType.accepted,
        )

    @on(Action.StatusNotification)
    async def on_status_notification(
        self,
        timestamp: str,
        connector_status: str,
        evse_id: int,
        connector_id: int,
    ) -> StatusNotificationPayload:
        logging.debug(f"{timestamp=} {connector_status=} {evse_id=} {connector_id=}")
        return StatusNotificationPayload()

    @on(Action.Heartbeat)
    async def on_heartbeat(self) -> HeartbeatPayload:
        return HeartbeatPayload(current_time=datetime.utcnow().isoformat())


def parse_path_id(path: str) -> str:
    """Parses the id from the path"""
    return unquote(path.strip("/"))


async def on_connect(websocket: WebSocketServerProtocol, path: str) -> None:
    """
    OCPP-compliant websocket handler. After stablishing websocket connection
    with the charge station (client), the protocol is delegated to this method.
    Creates a ChargePoint instance and start listening for messages.
    """
    try:
        requested_protocols = websocket.request_headers["Sec-WebSocket-Protocol"]
    except KeyError:
        logging.info("Client did not request any Subprotocol", "Closing connection")
        return await websocket.close()

    if websocket.subprotocol:
        logging.info(f"Protocols Matched: {websocket.subprotocol}")
    else:
        logging.warning(
            "No matching protocols",
            f"Server expects subprotocols: {websocket.available_subprotocols}",
            f"Client protocols:  {requested_protocols}",
            "Closing connection",
        )
        return await websocket.close()

    charge_point_id = parse_path_id(path)
    cp = ChargePoint(charge_point_id, websocket)
    await cp.start()
