import pytest

from app.city_filter import filter_cities_by_length

def test_filter_cities_by_length_exact_match():
    """Проверяет, что города ровно 5 символов не включаются."""
    cities_str = "Омск Уфа Рязань" # Рязань = 6
    filtered_cities = list(filter_cities_by_length(cities_str, min_length=5))
    assert filtered_cities == ["Рязань"]

def test_filter_cities_by_length_no_match():
    """Проверяет случай, когда нет подходящих городов."""
    cities_str = "Рим Милан Турин"
    filtered_cities = list(filter_cities_by_length(cities_str, min_length=5))
    assert len(filtered_cities) == 0
    assert filtered_cities == []

def test_filter_cities_by_length_empty_input():
    """Проверяет фильтрацию пустой строки."""
    cities_str = ""
    filtered_cities = list(filter_cities_by_length(cities_str, min_length=5))
    assert len(filtered_cities) == 0
    assert filtered_cities == []

def test_filter_cities_by_length_invalid_min_length():
    """Проверяет обработку недопустимой минимальной длины."""
    cities_str = "Москва"
    with pytest.raises(ValueError, match="Минимальная длина \(min_length\) не может быть отрицательной."):
        list(filter_cities_by_length(cities_str, min_length=-1))
