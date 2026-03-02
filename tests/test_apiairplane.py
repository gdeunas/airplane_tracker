from unittest.mock import Mock, patch

import pytest

from src.apiairplane import Aeroplane, AeroplanesAPI


def test_aeroplane():
    aeroplane = Aeroplane('A1', 'USA', 250.9, 1000.9)
    assert aeroplane.callsign == 'A1'
    assert aeroplane.origin_country == 'USA'
    assert aeroplane.velocity == 250.9
    assert aeroplane.altitude == 1000.9


def test_print_aeroplane():
    aeroplane = Aeroplane('A1', 'USA', 250.9, 1000.9)
    assert str(aeroplane) == 'Самолет: A1 (USA) | Скорость: 250.9 м/с | Высота: 1000.9 м'


def test_aeroplanes_compare():
    aeroplane1 = Aeroplane('A1', 'Spain', 200, 1000)
    aeroplane2 = Aeroplane('A2', 'Spain', 300, 1200)
    aeroplane3 = Aeroplane('A3', 'Spain', 200, 1000)

    assert (aeroplane1.is_faster_than(aeroplane2) == False)
    assert (aeroplane2.is_faster_than(aeroplane1) == True)

    assert aeroplane1 < aeroplane2
    assert aeroplane2.altitude == 1200

    assert aeroplane1 == aeroplane3

    # Проверяем, что при сравнении не с Aeroplane летит TypeError
    with pytest.raises(TypeError, match="Можно сравнивать только с объектом Aeroplane"):
        aeroplane1.is_faster_than("Not a plane")


def test_cats_empty():
    assert Aeroplane.cast_to_object_list(None) == []
    assert Aeroplane.cast_to_object_list([]) == []


def test_cast_to_object_list():
    aeroplane1 = Aeroplane('A1', 'Spain', 200, 1000)
    assert aeroplane1.callsign == 'A1'
    assert aeroplane1.origin_country == 'Spain'


def test_cast_to_object_list2():
    mock_data = [
        ["icao24", "A1", "USA", 17000000, 17000000, 0, 0, 0, False, 250.9, 0, 0, None, 1000.9],
        ["icao24", "B2", "Germany", 17000000, 17000000, 0, 0, 0, False, 300.0, 0, 0, None, 5000.0]
    ]

    result = Aeroplane.cast_to_object_list(mock_data)

    assert len(result) == 2
    assert result[0].callsign == 'A1'


def test_get_coordinates_success(api_instance):
    mock_response = Mock()
    mock_response.json.return_value = [{"boundingbox": ["55.0", "56.0", "37.0", "38.0"]}]

    with patch('requests.get', return_value=mock_response):
        coords = api_instance.get_coordinates("Russia")
        assert coords == [55.0, 56.0, 37.0, 38.0]


def test_get_aeroplanes_integration(api_instance):
    mock_coords = [{"boundingbox": ["10", "20", "30", "40"]}]
    mock_states = {"states": [["icao", "A1", "USA", 0, 0, 0, 0, 0, False, 250.0, 0, 0, None, 1000.0]]}

    with patch('requests.get') as mock_get:

        def side_effect(url, params=None, **kwargs):
            m = Mock()
            m.status_code = 200
            if "nominatim" in url:
                m.json.return_value = mock_coords
            else:
                m.json.return_value = mock_states
            return m

        mock_get.side_effect = side_effect

        result = api_instance.get_aeroplanes("USA")

        assert len(result) == 1
        assert result[0][1] == "A1"
