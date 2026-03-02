import pytest

from src.apiairplane import AeroplanesAPI
from src.apisave import JSONSaver


@pytest.fixture
def api_instance():
    return AeroplanesAPI()


@pytest.fixture
def temp_saver(tmp_path):
    """Создает временный JSON файл для тестов"""
    file_path = tmp_path / "test_planes.json"
    return JSONSaver(filename=str(file_path))


@pytest.fixture
def sample_plane():
    class MockAeroplane:
        callsign = "AFR123"
        origin_country = "France"
        velocity = 250.5
        altitude = 10000

    return MockAeroplane()


@pytest.fixture
def mock_planes():
    class Plane:
        def __init__(self, callsign, country, altitude):
            self.callsign = callsign
            self.origin_country = country
            self.altitude = altitude

    return [
        Plane("A1", "Russia", 1000),
        Plane("B2", "USA", 5000),
        Plane("C3", "Russia", 3000),
        Plane("D4", "France", None)
    ]
