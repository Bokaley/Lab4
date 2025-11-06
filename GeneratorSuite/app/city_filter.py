from typing import Generator, List

def filter_cities_by_length(city_string: str, min_length: int = 5) -> Generator[str, None, None]:
    """
    Принимает строку с названиями городов, разделенными пробелами,
    и возвращает генератор названий длиной более min_length.
    Исключительные ситуации:
    - Если city_string пустая, генератор просто ничего не вернет.
    - Если min_length < 0, выдает ValueError.
    """
    if min_length < 0:
        raise ValueError("Минимальная длина (min_length) не может быть отрицательной.")

    cities = city_string.split()
    for city in cities:
        if len(city) > min_length:
            yield city

# --- Использование фильтра ---
if __name__ == "__main__":
    cities_input = "Москва Питер Казань Уфа Омск Самара Ярославль Астрахань"

    print(f"--- Задание 3: Первые 3 города длиной более 5 символов ---")
    print(f"Входная строка: '{cities_input}'")

    try:
        city_gen = filter_cities_by_length(cities_input, min_length=5)

        # Извлекаем первые три значения с помощью next()
        first_city = next(city_gen)
        second_city = next(city_gen)
        third_city = next(city_gen)

        print(f"1: {first_city}")
        print(f"2: {second_city}")
        print(f"3: {third_city}")

    except ValueError as ve:
        print(f"Ошибка в параметрах фильтра: {ve}")
    except StopIteration:
        print("Не удалось извлечь 3 города, так как их меньше трех.")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
