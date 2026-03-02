def filter_aeroplanes(aeroplanes, countries):
    """Фильтрация по странам"""
    if not countries:
        return aeroplanes
    return [item for item in aeroplanes if item.origin_country in countries]


def get_aeroplanes_by_altitude(aeroplanes, altitude_range):
    """Фильтрация по высоте"""
    try:
        parts = altitude_range.split('-')
        min_alt = float(parts[0].strip())
        max_alt = float(parts[1].strip())
        return [item for item in aeroplanes if item.altitude and min_alt <= item.altitude <= max_alt]
    except ValueError:
        print("Некорректный диапазон высот")
        return aeroplanes


def sort_aeroplanes(aeroplanes):
    """Сортировка по высоте"""
    return sorted(aeroplanes, key=lambda item: item.altitude if item.altitude else 0, reverse=True)


def get_top_aeroplanes(aeroplanes, top_n):
    """Возврат первые n самолетов"""
    return aeroplanes[:top_n]


def print_aeroplanes(aeroplanes):
    """Вывод списка самолетов"""
    if not aeroplanes:
        print("Самолеты не найдены")
        return
    for i, a in enumerate(aeroplanes, 1):
        print(f"{i}. Позывной: {a.callsign} | Страна: {a.origin_country} | Высота: {a.altitude} м")
