import requests
from urllib.parse import quote
from typing import Any, Dict, Optional
from dataclasses import dataclass
import re


@dataclass
class SensorApiClient:
    base_url: str = "http://192.168.1.5:8000"
    timeout: float = 5.0

    def __post_init__(self):
        self._session = requests.Session()
        self._session.headers.update({"accept": "application/json"})

    def close(self):
        try:
            self._session.close()
        except Exception:
            pass

    def _url(self, mac: str) -> str:
        return f"{self.base_url}/sensor/{quote(mac, safe='')}/last/"

    def fetch_last(self, mac: str) -> Dict[str, Any]:
        """Отримати десеріалізований JSON для /sensor/{mac}/last/. Повертає блок 'ok' якщо є."""
        resp = self._session.get(self._url(mac), timeout=self.timeout)
        resp.raise_for_status()
        data = resp.json()
        return data.get("ok", data)

    @staticmethod
    def extract_channel(payload: Dict[str, Any], index: int) -> Optional[float]:
        """Значення каналу (1-індексація) з body.channels."""
        channels = (payload.get("body") or {}).get("channels") or []
        try:
            return channels[index - 1]
        except (IndexError, TypeError):
            return None

    @staticmethod
    def extract_unit(payload: Dict[str, Any], index: int) -> Optional[str]:
        """Одиниця виміру для каналу (1-індексація) з header.unit."""
        units = (payload.get("header") or {}).get("unit") or []
        try:
            return units[index - 1]
        except (IndexError, TypeError):
            return None

    @staticmethod
    def extract_channel_name(payload: Dict[str, Any], index: int) -> Optional[str]:
        """Назва каналу (1-індексація) з header.channel_name."""
        names = (payload.get("header") or {}).get("channel_name") or []
        try:
            return names[index - 1]
        except (IndexError, TypeError):
            return None

    @staticmethod
    def _to_str(v: Any) -> str:
        return "" if v is None else str(v)

    def get_channel(self, mac: str, index: int) -> list[str]:
        """
        Повертає [channel_name, value, unit] як рядки для каналу (1-індексація).
        Завжди повертає три елементи, None → "".
        """
        try:
            payload = self.fetch_last(mac)
            name = self.extract_channel_name(payload, index)
            val = self.extract_channel(payload, index)
            unit = self.extract_unit(payload, index)
        except Exception:
            name = val = unit = None
        return [self._to_str(name), self._to_str(val), self._to_str(unit)]

    def get_switch_state(self, switch_id: int) -> Optional[Dict[str, Any]]:
        """
        Отримати стан свіча за ID.
        Повертає словник з полями: id, switch_name, state, enabled, state_changed_at, changed_by, description
        або None у разі помилки.
        """
        try:
            url = f"{self.base_url}/getSwitchesById/"
            params = {"switch_id": switch_id}
            resp = self._session.get(url, params=params, timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()
            return data.get("ok")
        except Exception as e:
            print(f"Error fetching switch state: {e}")
            return None
    def set_switch_state(self, switch_id: int, state: bool, user_key: str = "key") -> bool:
        """
        Задати стан свіча за ID.
        Повертає True якщо операція успішна, False якщо помилка.
        """
        try:
            url = f"{self.base_url}/setSwitchById/"
            params = {
                "switch_id": switch_id,
                "state": "true" if state else "false",
                "userKey": user_key
            }
            resp = self._session.get(url, params=params, timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()
        # Перевіряємо чи є "ok" в відповіді
            return "ok" in data
        except Exception as e:
            print(f"Error setting switch state: {e}")
            return False



    def oldApiGetData(self):
        """Старий API для отримання даних сенсора."""
        try:
            response = self._session.get("http://ip-service.net.ua/get_telemetry.php", timeout=self.timeout)
            if response.status_code == 200:
                return re.sub(r'[^!-~a-zA-Z0-9]', '', response.content.decode('utf-8'))
        except requests.RequestException as e:
            print(f"Error fetching sensor data: {e}")
            return None

if __name__ == "__main__":
    # Простий CLI для індивідуального тесту
    import argparse, json, os, sys

    

    client = SensorApiClient(base_url="http://192.168.1.5:8000")
    #var = json.dumps(client.fetch_last("Battery:0x0003"), indent=2, ensure_ascii=False)
    #print(var)
    channel = client.get_channel("Battery:0x0003", 5)
    channel.append("FFFFFF")
    print(f"Channel 1 value: {channel}")
    client.close()