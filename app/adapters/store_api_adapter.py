import json
import logging
from typing import List

import pydantic_core
import requests

from app.entities.processed_agent_data import ProcessedAgentData
from app.interfaces.store_gateway import StoreGateway


class StoreApiAdapter(StoreGateway):
    def __init__(self, api_base_url):
        self.api_base_url = api_base_url

    def save_data(self, processed_agent_data_batch: List[ProcessedAgentData]):
        endpoint_url = f"{self.api_base_url}/processed_agent_data/"
        try:
            response = self._send_data(endpoint_url, processed_agent_data_batch)
            if response and response.status_code in (200, 201):
                logging.info("Processed data saved successfully.")
                return True
            else:
                logging.info(
                    f"Failed to save processed data. Status code: {response.status_code if response else 'Unknown'}"
                )
                return False
        except requests.exceptions.RequestException as e:
            logging.info(f"Failed to connect to the Store API: {e}")
            return False
