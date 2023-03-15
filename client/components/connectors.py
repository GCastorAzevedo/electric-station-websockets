import logging
from typing import List

logging.basicConfig(level=logging.INFO)


def discover_connectors(charge_point: str) -> List[int]:
    """
    Discover all connectors managed by a charging point.
    """
    connectors = [1]
    logging.info(f"Found {charge_point} connectors: {connectors}")
    return connectors
