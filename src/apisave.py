# src/apisave.py
import json
import os
from abc import ABC, abstractmethod

from src.apiairplane import Aeroplane


class BaseSaver(ABC):
    """Абстрактный класс для сохранения"""

    @abstractmethod
    def add_aeroplane(self, aeroplane: Aeroplane):
        pass

    @abstractmethod
    def get_aeroplane(self, criteria: dict):
        pass

    @abstractmethod
    def delete_aeroplane(self, aeroplane: Aeroplane):
        pass


class JSONSaver(BaseSaver):
    """Класс для сохранения данных о самолетах в формате json"""

    def __init__(self, filename="aeroplane.json"):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=4)

    def add_aeroplane(self, aeroplane):
        """Добавляем один самолет в json файл"""
        data = self._read_file()
        plane_dict = {
            "callsign": aeroplane.callsign,
            "origin_country": aeroplane.origin_country,
            "velocity": aeroplane.velocity,
            "altitude": aeroplane.altitude,
        }

        data.append(plane_dict)
        self._write_file(data)

    def get_aeroplane(self, criteria: dict):
        """Вывод спискок самолетов по критериям"""
        data = self._read_file()
        return [
            item for item in data if all(item.get(k) == v for k, v in criteria.items())
        ]

    def delete_aeroplane(self, aeroplane):
        data = self._read_file()
        new_data = [item for item in data if item.get("callsign") != aeroplane.callsign]
        self._write_file(new_data)

    def _read_file(self):
        """чтение данных"""
        with open(self.filename, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write_file(self, data):
        """запись данных"""
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
