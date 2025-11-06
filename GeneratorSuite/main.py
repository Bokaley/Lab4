import sys
from string import ascii_lowercase
from typing import Generator, Iterator, Tuple, List

from app.generators import generate_two_letter_combinations, generate_function_values, f
from app.city_filter import filter_cities_by_length

def main_console():
    """
    Главная функция для консольного запуска.
    """
    print("--- GeneratorSuite: Консольная версия ---")

    # --- Задание 1 ---
    print("\n--- Задание 1: Первые 50 сочетаний из двух букв ---")
    combinations_gen = generate_two_letter_combinations()
    count = 0
    for combination in combinations_gen:
        if count >= 50:
            break
        print(combination, end=" ")
        count += 1
    print("\n" + "="*50)

    # --- Задание 2 ---
    print("\n--- Задание 2: Первые 20 значений функции f(x) ---")
    try:
        # Определяем параметры a и b
        a_param = -5.0
        b_param = 7.0
        step_param = 0.01

        func_gen = generate_function_values(a=a_param, b=b_param, step=step_param)
        print(f"Диапазон: [{a_param}, {b_param}], Шаг: {step_param}")
        count = 0
        for value in func_gen:
            if count >= 20:
                break
            print(f"{count+1}: {value:.4f}") # Форматируем вывод
            count += 1
    except ValueError as ve:
        print(f"Ошибка в параметрах генератора: {ve}", file=sys.stderr)
    except Exception as e:
        print(f"Произошла непредвиденная ошибка при вычислении функции: {e}", file=sys.stderr)
    print("="*50)

    # --- Задание 3 ---
    print("\n--- Задание 3: Первые 3 города длиной более 5 символов ---")
    cities_input = "Москва Питер Казань Уфа Омск Самара Ярославль Астрахань"
    min_len_city = 5
    print(f"Входная строка: '{cities_input}'")

    try:
        city_gen = filter_cities_by_length(cities_input, min_length=min_len_city)

        # Извлекаем первые три значения с помощью next()
        print(f"Фильтр: длина > {min_len_city} символов")
        try:
            first_city = next(city_gen)
            second_city = next(city_gen)
            third_city = next(city_gen)

            print(f"1: {first_city}")
            print(f"2: {second_city}")
            print(f"3: {third_city}")

        except StopIteration:
            print("Не удалось извлечь 3 города, так как их меньше трех.")

    except ValueError as ve:
        print(f"Ошибка в параметрах фильтра: {ve}", file=sys.stderr)
    except Exception as e:
        print(f"Произошла непредвиденная ошибка при фильтрации городов: {e}", file=sys.stderr)
    print("="*50)

if __name__ == "__main__":
    main_console()
