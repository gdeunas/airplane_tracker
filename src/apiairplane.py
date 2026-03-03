from abc import ABC, abstractmethod
from typing import Any

import requests


class BaseAPI(ABC):
    """Абстрактный класс для работы с внешними API"""

    @abstractmethod
    def get_coordinates(self, country_name: str):
        pass

    @abstractmethod
    def get_aeroplanes(self, country_name: str):
        pass


class AeroplanesAPI(BaseAPI):
    """Реализация работы с Nominatim и OpenSky Network"""

    def __init__(self):
        self.nominatim_url = "https://nominatim.openstreetmap.org/search"
        self.opensky_url = "https://opensky-network.org/api/states/all?"
        self.headers = {"User-Agent": "Airplane_tracker/1.0"}

    def get_coordinates(self, country_name: str):
        """Получает ограничивающую рамку (bounding box) страны"""
        params: dict[str, Any] = {"country": country_name, "format": "json", "limit": 1}
        response = requests.get(self.nominatim_url, params=params, headers=self.headers)
        data = response.json()

        if data:
            # Возвращает [min_lat, max_lat, min_lon, max_lon]
            bbox = data[0].get("boundingbox")
            return [float(x) for x in bbox]
        return None

    def get_aeroplanes(self, country_name: str):
        """Получает самолеты в небе конкретной страны по её координатам"""
        bbox = self.get_coordinates(country_name)
        if not bbox:
            print(f"Координаты для {country_name} не найдены.")
            return []

        # OpenSky требует: lamin, lomin, lamax, lomax
        params = {
            "lamin": bbox[0],
            "lamax": bbox[1],
            "lomin": bbox[2],
            "lomax": bbox[3],
        }

        response = requests.get(self.opensky_url, params=params)
        if response.status_code == 200:
            states = response.json().get("states")
            return states if states else []
        return []


class Aeroplane:
    """Класс о данных самолетах"""

    __slots__ = ("_callsign", "_origin_country", "_velocity", "_altitude")

    def __init__(
        self, callsign: str, origin_country: str, velocity: float, altitude: float
    ):
        self._callsign = callsign.strip() if callsign else "N/A"  # позывной
        self._origin_country = origin_country  # страна регистрации
        self._velocity = velocity if velocity is not None else 0.0  # скорость полета
        self._altitude = altitude if altitude is not None else 0.0  # высота полета

    @property
    def callsign(self):
        return self._callsign

    @property
    def origin_country(self):
        return self._origin_country

    @property
    def velocity(self):
        return self._velocity

    @property
    def altitude(self):
        return self._altitude

    @classmethod
    def cast_to_object_list(cls, data):
        """Преобразует список списков из API OpenSky в список объектов Aeroplane"""
        if not data:
            return []
        return [cls(item[1], item[2], item[9], item[13]) for item in data]

    # Сравнение по высоте (altitude)
    def __lt__(self, other):
        return self.altitude < other.altitude

    def __eq__(self, other):
        return self.altitude == other.altitude and self.velocity == other.velocity

    # Сравнение по скорости (velocity)
    def is_faster_than(self, other):
        if not isinstance(other, Aeroplane):
            raise TypeError("Можно сравнивать только с объектом Aeroplane")
        return self.velocity > other.velocity

    def __repr__(self):
        return (
            f"Самолет: {self._callsign} ({self._origin_country}) | "
            f"Скорость: {self._velocity} м/с | Высота: {self._altitude} м"
        )


# if __name__ == "__main__":
# api = AeroplanesAPI()
# airplane = api.get_aeroplanes("United States")
# airplanes = Aeroplane.cast_to_object_list(airplane)
# for plane in airplanes[:5]:
#     print(plane)
