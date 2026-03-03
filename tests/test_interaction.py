import pytest

from src.interaction_user import filter_aeroplanes, get_top_aeroplanes, sort_aeroplanes, \
    get_aeroplanes_by_altitude


def test_filter_aeroplanes(mock_planes):
    result = filter_aeroplanes(mock_planes, ["Russia"])
    assert len(result) == 2
    assert all(p.origin_country == "Russia" for p in result)

    assert len(filter_aeroplanes(mock_planes, [])) == 4


@pytest.mark.parametrize("range_str, expected_count", [
    ("1000-4000", 2),  # A1 и C3
    ("0-10000", 3),  # Кроме D4 (у него None)
    ("invalid", 4),  # Некорректный ввод возвращает исходный список
])
def test_get_aeroplanes_by_altitude(mock_planes, range_str, expected_count):
    result = get_aeroplanes_by_altitude(mock_planes, range_str)
    assert len(result) == expected_count


def test_sort_aeroplanes(mock_planes):
    sorted_list = sort_aeroplanes(mock_planes)
    assert sorted_list[0].callsign == "B2"
    assert sorted_list[-1].callsign == "D4"


def test_get_top_aeroplanes(mock_planes):
    top_2 = get_top_aeroplanes(mock_planes, 2)
    assert len(top_2) == 2
    assert top_2[0].callsign == "A1"
