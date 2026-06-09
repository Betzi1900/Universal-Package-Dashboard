# dhl_api.py
import requests
import xml.etree.ElementTree as ET
import os
import json
import base64


class DHLTracker:
    def __init__(self):
        self.api_url = "https://api-eu.dhl.com/parcel/de/tracking/v0/shipments"
        self.api_key, self.api_secret = self.load_credentials()

    def load_credentials(self):
        if os.path.exists("config.json"):
            try:
                with open("config.json", "r") as f:
                    config = json.load(f)
                    return config.get("dhl_api_key", "").strip(), config.get("dhl_api_secret", "").strip()
            except Exception:
                return "", ""
        return "", ""

    def track(self, tracking_number):
        if not self.api_key or not self.api_secret:
            return {"error": "DHL Key oder Secret fehlen in der config.json."}

        tracking_number = str(tracking_number).strip()

        xml_payload = f'''<?xml version="1.0" encoding="UTF-8"?>
<data request="get-status-for-public-user" language-code="de">
    <data piece-code="{tracking_number}" />
</data>'''

        params = {"xml": xml_payload}
        auth_str = f"{self.api_key}:{self.api_secret}"
        encoded_auth = base64.b64encode(auth_str.encode()).decode()

        headers = {
            "Authorization": f"Basic {encoded_auth}",
            "DHL-API-Key": self.api_key,
            "Accept": "application/xml"
        }

        try:
            response = requests.get(self.api_url, headers=headers, params=params)

            if response.status_code == 200:
                try:
                    root = ET.fromstring(response.text)
                    status_node = None
                    for elem in root.iter('data'):
                        if elem.get('name') == 'piece-status-public':
                            status_node = elem
                            break

                    if status_node is not None:
                        status = status_node.get('status', 'Status unbekannt')
                        time_from = status_node.get('delivery-timeframe-from', '')
                        time_to = status_node.get('delivery-timeframe-to', '')
                        timeframe = f" ({time_from} - {time_to} Uhr)" if time_from and time_to else ""

                        return {"shipment": {"status": f"{status}{timeframe}", "sender": "DHL Paket"}}
                    else:
                        return {"error": "Paket in der DHL-Datenbank nicht gefunden."}
                except ET.ParseError:
                    return {"error": "Ungültiges XML Format von DHL empfangen."}

            return {"error": f"API Fehler {response.status_code}"}

        except Exception as e:
            return {"error": f"Verbindungsfehler: {e}"}