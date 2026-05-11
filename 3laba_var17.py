"""
Лабораторная работа №3. Файлы и словари.
Вариант 17. История перемещений офисных работников.
Поля: №, дата и время, признак рабочего места (bool), номер комнаты.

Выполняет:
1) Подсчёт количества файлов в указанной папке.
2) Чтение данных из CSV-файла в список словарей.
3) Вывод записей, отсортированных по строковому полю (дата и время как строка).
4) Вывод записей, отсортированных по числовому полю (номер записи).
5) Вывод записей по критерию (признак рабочего места = True).
6) Добавление новой записи и сохранение в файл.
"""

import os
import csv
from datetime import datetime


def count_files_in_directory(directory="."):
    try:
        items = os.listdir(directory)
        files = [item for item in items if os.path.isfile(os.path.join(directory, item))]
        return len(files)
    except FileNotFoundError:
        print(f"Директория '{directory}' не найдена.")
        return 0
    except PermissionError:
        print(f"Нет доступа к директории '{directory}'.")
        return 0


def read_csv_to_dict_list(filepath):
    data = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Преобразование типов
                row['id'] = int(row['id'])
                row['at_workplace'] = row['at_workplace'].strip().lower() == 'true'
                row['room_number'] = int(row['room_number'])
                data.append(row)
        return data
    except FileNotFoundError:
        print(f"Файл '{filepath}' не найден. Будет создан новый при сохранении.")
        return []


def print_records(records):
    if not records:
        print("Нет данных для отображения.")
        return
    print(f"{'№':<5} {'Дата и время':<22} {'На месте':<10} {'Комната':<10}")
    print("-" * 50)
    for r in records:
        print(f"{r['id']:<5} {r['datetime']:<22} {str(r['at_workplace']):<10} {r['room_number']:<10}")
    print()


def sort_by_string_field(data):
    return sorted(data, key=lambda x: x['datetime'])


def sort_by_numeric_field(data):
    return sorted(data, key=lambda x: x['id'])


def filter_by_criterion(data, field, value):
    return [r for r in data if r.get(field) == value]


def add_new_record(data, filepath):
    print("Добавление новой записи.")
    try:
        # Ввод данных
        record = {}
        max_id = max((r['id'] for r in data), default=0)
        record['id'] = max_id + 1
        print(f"Присвоен номер: {record['id']}")

        while True:
            dt_str = input("Введите дату и время в формате ГГГГ-ММ-ДД ЧЧ:ММ:СС: ").strip()
            try:
                datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
                record['datetime'] = dt_str
                break
            except ValueError:
                print("Неверный формат. Пример: 2025-04-01 12:30:45")

        while True:
            wp = input("Работник на рабочем месте? (да/нет): ").strip().lower()
            if wp in ('да', 'yes', 'y', 'true'):
                record['at_workplace'] = True
                break
            elif wp in ('нет', 'no', 'n', 'false'):
                record['at_workplace'] = False
                break
            else:
                print("Введите 'да' или 'нет'.")

        while True:
            try:
                record['room_number'] = int(input("Номер комнаты (целое число): "))
                break
            except ValueError:
                print("Ошибка: введите целое число.")

        data.append(record)

        file_exists = os.path.isfile(filepath)
        with open(filepath, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['id', 'datetime', 'at_workplace', 'room_number'])
            if not file_exists:
                writer.writeheader()
            writer.writerow(record)

        print("Запись успешно добавлена.\n")
    except Exception as e:
        print(f"Ошибка при добавлении записи: {e}")


def create_example_csv(filepath):
    """Создаёт пример CSV-файла, если его нет."""
    if not os.path.isfile(filepath):
        sample_data = [
            {'id': 1, 'datetime': '2025-04-01 09:15:00', 'at_workplace': 'True', 'room_number': 101},
            {'id': 2, 'datetime': '2025-04-01 10:30:00', 'at_workplace': 'False', 'room_number': 202},
            {'id': 3, 'datetime': '2025-04-01 08:45:00', 'at_workplace': 'True', 'room_number': 101},
            {'id': 4, 'datetime': '2025-04-02 11:00:00', 'at_workplace': 'True', 'room_number': 303},
            {'id': 5, 'datetime': '2025-04-02 09:00:00', 'at_workplace': 'False', 'room_number': 404},
        ]
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['id', 'datetime', 'at_workplace', 'room_number'])
            writer.writeheader()
            writer.writerows(sample_data)
        print(f"Создан пример файла '{filepath}'.")


def main():
    print("Лабораторная работа №3. Вариант 17. История перемещений офисных работников.\n")

    directory = input("Введите путь к папке для подсчёта файлов (Enter - текущая): ").strip()
    if not directory:
        directory = "."
    file_count = count_files_in_directory(directory)
    print(f"Количество файлов в папке '{directory}': {file_count}\n")

    csv_filename = "data.csv"
    create_example_csv(csv_filename)

    records = read_csv_to_dict_list(csv_filename)
    print(f"Загружено {len(records)} записей из файла '{csv_filename}'.\n")

    while True:
        print("Выберите действие:")
        print("1 - Вывести записи, отсортированные по дате и времени (строковое поле)")
        print("2 - Вывести записи, отсортированные по номеру (числовое поле)")
        print("3 - Вывести записи, где работник на рабочем месте (критерий)")
        print("4 - Добавить новую запись")
        print("5 - Выход")
        choice = input("Ваш выбор: ").strip()

        if choice == '1':
            sorted_records = sort_by_string_field(records)
            print("\nЗаписи, отсортированные по дате и времени (как строка):")
            print_records(sorted_records)
        elif choice == '2':
            sorted_records = sort_by_numeric_field(records)
            print("\nЗаписи, отсортированные по номеру (числовое поле):")
            print_records(sorted_records)
        elif choice == '3':
            filtered = filter_by_criterion(records, 'at_workplace', True)
            print("\nЗаписи, где работник на рабочем месте:")
            print_records(filtered)
        elif choice == '4':
            add_new_record(records, csv_filename)
        elif choice == '5':
            print("Выход.")
            break
        else:
            print("Неверный ввод. Попробуйте снова.\n")


if __name__ == "__main__":
    main()