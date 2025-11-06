import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QLabel, QPushButton, QLineEdit, QSpinBox, QDoubleSpinBox,
    QTextEdit, QListWidget, QListWidgetItem, QGridLayout, QMessageBox
)
from PySide6.QtCore import Qt, Slot, QThread, Signal
from typing import Generator, Iterator, List, Optional, Tuple # Импортируем для аннотаций

# Импортируем наши генераторы и фильтры
from app.generators import generate_two_letter_combinations, generate_function_values, f
from app.city_filter import filter_cities_by_length

# --- Вспомогательный класс для многопоточности (для UI) ---
# Этот класс поможет вынести долгие операции в отдельный поток,
# чтобы UI не зависал.

class GeneratorWorker(QThread):
    # Сигналы для передачи результатов обратно в UI поток
    progress_combination = Signal(str)
    progress_function_value = Signal(float)
    progress_city = Signal(str)
    finished_combinations = Signal()
    finished_function_values = Signal()
    finished_cities = Signal()
    error_occurred = Signal(str) # Сигнал для передачи сообщений об ошибках

    def __init__(self, parent=None):
        super().__init__(parent)
        self._running = False
        self._generators = {} # Словарь для хранения ссылок на генераторы

    def run(self):
        self._running = True
        try:
            # Обработка Задания 1
            if 'combinations' in self._generators:
                gen = self._generators['combinations']
                for i, item in enumerate(gen):
                    if not self._running: break
                    if i < 50: # Выводим только первые 50, как в условии
                        self.progress_combination.emit(item)
                    else:
                        break # Останавливаемся после 50
                self.finished_combinations.emit()

            # Обработка Задания 2
            if 'function_values' in self._generators:
                gen = self._generators['function_values']
                for i, value in enumerate(gen):
                    if not self._running: break
                    if i < 20: # Выводим только первые 20
                        self.progress_function_value.emit(value)
                    else:
                        break # Останавливаемся после 20
                self.finished_function_values.emit()

            # Обработка Задания 3
            if 'cities' in self._generators:
                gen = self._generators['cities']
                # Извлекаем первые 3 значения
                try:
                    for _ in range(3):
                        if not self._running: break
                        city = next(gen)
                        self.progress_city.emit(city)
                    # Если генератор закончился раньше, это нормально
                except StopIteration:
                    pass # Просто заканчиваем, если городов меньше 3
                self.finished_cities.emit()

        except Exception as e:
            self.error_occurred.emit(f"Ошибка в рабочем потоке: {e}")
        finally:
            self._running = False
            # Очищаем использованные генераторы
            self._generators.clear()

    def set_generators(self, generators: dict):
        """
        Устанавливает генераторы, которые нужно выполнить.
        :param generators: Словарь вида {'name': generator_object}
        """
        self._generators = generators

    def stop(self):
        self._running = False

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("GeneratorSuite")
        self.setGeometry(100, 100, 800, 600) # x, y, width, height

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)

        self.init_task1_tab()
        self.init_task2_tab()
        self.init_task3_tab()

        # --- Worker для многопоточности ---
        self.worker = GeneratorWorker(self)
        self.worker.progress_combination.connect(self.add_to_task1_output)
        self.worker.progress_function_value.connect(self.add_to_task2_output)
        self.worker.progress_city.connect(self.add_to_task3_output)
        self.worker.finished_combinations.connect(self.on_task1_finished)
        self.worker.finished_function_values.connect(self.on_task2_finished)
        self.worker.finished_cities.connect(self.on_task3_finished)
        self.worker.error_occurred.connect(self.show_error_message)

    def init_task1_tab(self):
        """Инициализация вкладки для Задания 1."""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        self.task1_output = QTextEdit()
        self.task1_output.setReadOnly(True)
        layout.addWidget(self.task1_output)

        btn_run = QPushButton("Выполнить Задание 1 (Первые 50)")
        btn_run.setObjectName("btn_run_task1")
        btn_run.clicked.connect(self.run_task1)
        layout.addWidget(btn_run)

        self.tab_widget.addTab(tab, "Комбинации Букв")

    def init_task2_tab(self):
        """Инициализация вкладки для Задания 2."""
        tab = QWidget()
        layout = QGridLayout(tab) # Используем QGridLayout для лучшего расположения

        layout.addWidget(QLabel("Диапазон [a; b]"), 0, 0)

        self.task2_a_input = QDoubleSpinBox()
        self.task2_a_input.setRange(-1000.0, 1000.0)
        self.task2_a_input.setSingleStep(0.1)
        self.task2_a_input.setValue(-5.0) # Значение по умолчанию
        layout.addWidget(self.task2_a_input, 0, 1)

        self.task2_b_input = QDoubleSpinBox()
        self.task2_b_input.setRange(-1000.0, 1000.0)
        self.task2_b_input.setSingleStep(0.1)
        self.task2_b_input.setValue(7.0) # Значение по умолчанию
        layout.addWidget(self.task2_b_input, 0, 2)

        layout.addWidget(QLabel("Шаг"), 1, 0)
        self.task2_step_input = QDoubleSpinBox()
        self.task2_step_input.setRange(0.001, 10.0) # Шаг должен быть > 0
        self.task2_step_input.setSingleStep(0.001)
        self.task2_step_input.setValue(0.01)
        layout.addWidget(self.task2_step_input, 1, 1)

        btn_run = QPushButton("Выполнить Задание 2 (Первые 20)")
        btn_run.setObjectName("btn_run_task2")
        btn_run.clicked.connect(self.run_task2)
        layout.addWidget(btn_run, 2, 0, 1, 3) # Растягиваем кнопку на 3 колонки

        self.task2_output = QTextEdit()
        self.task2_output.setReadOnly(True)
        layout.addWidget(self.task2_output, 3, 0, 1, 3)

        self.tab_widget.addTab(tab, "Значения Функции")

    def init_task3_tab(self):
        """Инициализация вкладки для Задания 3."""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        self.task3_input_cities = QLineEdit()
        self.task3_input_cities.setPlaceholderText("Введите названия городов через пробел")
        self.task3_input_cities.setText("Москва Питер Казань Уфа Омск Самара Ярославль Астрахань") # Значение по умолчанию
        layout.addWidget(self.task3_input_cities)

        layout.addWidget(QLabel("Минимальная длина названия города:"))
        self.task3_min_len_input = QSpinBox()
        self.task3_min_len_input.setRange(1, 100)
        self.task3_min_len_input.setValue(5)
        layout.addWidget(self.task3_min_len_input)

        btn_run = QPushButton("Выполнить Задание 3 (Первые 3)")
        btn_run.setObjectName("btn_run_task3")
        btn_run.clicked.connect(self.run_task3)
        layout.addWidget(btn_run)

        self.task3_output = QTextEdit()
        self.task3_output.setReadOnly(True)
        layout.addWidget(self.task3_output)

        self.tab_widget.addTab(tab, "Фильтр Городов")

    # --- Методы для запуска генераторов ---

    def run_task1(self):
        """Запускает генератор комбинаций в отдельном потоке."""
        self.task1_output.clear()
        self.task1_output.append("Запуск генерации...")
        self.worker.set_generators({'combinations': generate_two_letter_combinations()})
        self.worker.start()
        # Кнопка должна быть отключена во время выполнения
        btn = self.findChild(QPushButton, "btn_run_task1")

    def run_task2(self):
        """Запускает генератор значений функции в отдельном потоке."""
        self.task2_output.clear()
        a = self.task2_a_input.value()
        b = self.task2_b_input.value()
        step = self.task2_step_input.value()

        if step <= 0:
            self.show_error_message("Ошибка: Шаг должен быть положительным.")
            return
        if a > b:
            self.show_error_message("Ошибка: Начальное значение 'a' не может быть больше конечного 'b'.")
            return

        self.task2_output.append(f"Запуск для a={a}, b={b}, step={step}...")
        try:
            # Важно: нужно создать новый генератор каждый раз,
            # так как генераторы конечны.
            func_gen = generate_function_values(a=a, b=b, step=step)
            self.worker.set_generators({'function_values': func_gen})
            self.worker.start()
            # Отключаем кнопку
            btn = self.findChild(QPushButton, "btn_run_task2")
        except ValueError as ve:
            self.show_error_message(f"Ошибка параметров: {ve}")
        except Exception as e:
            self.show_error_message(f"Непредвиденная ошибка: {e}")

    def run_task3(self):
        """Запускает фильтр городов в отдельном потоке."""
        self.task3_output.clear()
        cities_str = self.task3_input_cities.text()
        min_len = self.task3_min_len_input.value()

        if not cities_str:
            self.task3_output.append("Введите названия городов.")
            return

        try:
            # Создаем генератор фильтра
            city_gen = filter_cities_by_length(cities_str, min_length=min_len)
            self.worker.set_generators({'cities': city_gen})
            self.worker.start()
            # Отключаем кнопку
            btn = self.findChild(QPushButton, "btn_run_task3")
        except ValueError as ve:
            self.show_error_message(f"Ошибка параметров: {ve}")
        except Exception as e:
            self.show_error_message(f"Непредвиденная ошибка: {e}")


    # --- Слоты для получения данных от Worker ---

    @Slot(str)
    def add_to_task1_output(self, combination):
        self.task1_output.append(combination)

    @Slot(float)
    def add_to_task2_output(self, value):
        self.task2_output.append(f"{value:.4f}")

    @Slot(str)
    def add_to_task3_output(self, city):
        self.task3_output.append(city)

    # --- Слоты для завершения работы ---

    @Slot()
    def on_task1_finished(self):
        self.task1_output.append("\nГенерация комбинаций завершена.")
        btn = self.findChild(QPushButton, "btn_run_task1")

    @Slot()
    def on_task2_finished(self):
        self.task2_output.append("\nГенерация значений функции завершена.")
        btn = self.findChild(QPushButton, "btn_run_task2")

    @Slot()
    def on_task3_finished(self):
        self.task3_output.append("\nФильтрация городов завершена.")
        btn = self.findChild(QPushButton, "btn_run_task3")
    # --- Обработка ошибок ---
    @Slot(str)
    def show_error_message(self, message):
        QMessageBox.critical(self, "Ошибка", message)
        # Включаем кнопки обратно, если произошла ошибка
        self.tab_widget.findChild(QPushButton, "Выполнить Задание 1 (Первые 50)").setEnabled(True)
        self.tab_widget.findChild(QPushButton, "Выполнить Задание 2 (Первые 20)").setEnabled(True)
        self.tab_widget.findChild(QPushButton, "Выполнить Задание 3 (Первые 3)").setEnabled(True)

    def closeEvent(self, event):
        """
        Обработка закрытия окна. Останавливаем worker, если он работает.
        """
        if self.worker.isRunning():
            self.worker.stop()
            self.worker.wait() # Ждем завершения потока
        event.accept()
