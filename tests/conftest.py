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
