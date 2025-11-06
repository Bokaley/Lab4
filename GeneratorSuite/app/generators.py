import sys
from string import ascii_lowercase
from typing import Generator, Iterator, Tuple, List

# --- Задание 1: Все сочетания из двух букв ---

def generate_two_letter_combinations() -> Generator[str, None, None]:
    """
    Генерирует все сочетания из двух латинских букв (малых).
    """
    for char1 in ascii_lowercase:
        for char2 in ascii_lowercase:
            yield char1 + char2

# --- Задание 2: Функция f(x) = 0.1x^2 + 5x - 2 ---

def f(x: float) -> float:
    """
    Математическая функция f(x) = 0.1x^2 + 5x - 2.
    """
    return 0.1 * x**2 + 5 * x - 2

def generate_function_values(a: float, b: float, step: float = 0.01) -> Generator[float, None, None]:
    """
    Генерирует значения функции f(x) в диапазоне [a, b] с заданным шагом.
    Исключительные ситуации:
    - Если step <= 0, выдает ValueError.
    - Если a > b, выдает ValueError.
    - Исключительные ситуации при вычислении f(x) (например, деление на ноль, если бы оно было)
      будут вызваны напрямую Python (например, OverflowError, TypeError),
      но в данной функции f(x) они маловероятны.
    """
    if step <= 0:
        raise ValueError("Шаг (step) должен быть положительным.")
    if a > b:
        raise ValueError("Начальное значение диапазона (a) не может быть больше конечного (b).")

    current_x = a
    while current_x <= b:
        try:
            value = f(current_x)
            yield value
        except Exception as e:
            # Обрабатываем любые возможные ошибки при вычислении функции
            print(f"Ошибка при вычислении f({current_x}): {e}", file=sys.stderr)
            # Можно решить, что делать дальше: пропустить, остановить генератор
            # В данном случае, просто пропустим это значение и продолжим
        current_x += step

# --- Использование генераторов ---
if __name__ == "__main__":
    print("--- Задание 1: Первые 50 сочетаний из двух букв ---")
    combinations_gen = generate_two_letter_combinations()
    for i in range(50):
        try:
            print(next(combinations_gen), end=" ")
        except StopIteration:
            break
    print("\n" + "="*50)

    print("\n--- Задание 2: Первые 20 значений функции f(x) ---")
    try:
        func_gen = generate_function_values(a=-5, b=7, step=0.01)
        for i in range(20):
            print(f"{i+1}: {next(func_gen):.4f}") # Форматируем вывод
    except ValueError as ve:
        print(f"Ошибка в параметрах генератора: {ve}")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
    print("="*50)
