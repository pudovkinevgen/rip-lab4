"""
Лабораторная работа №4. Классы.
Вариант 17. История перемещений офисных работников.
Поля: №, дата и время, признак рабочего места (bool), номер комнаты.

Реализовано:
- Класс записи OfficeMovement с контролем установки атрибутов через __setattr__.
- Класс-коллекция MovementCollection с итератором, __getitem__, __repr__, генераторами.
- Наследование: FilteredCollection (коллекция только записей "на рабочем месте").
- Статические методы: валидация даты/времени, преобразование строки в bool.
"""

# Второй коммит: демонстрация изменений
# Экспериментальная сортировка
# Дополнительный фильтр

import os
import csv
from datetime import datetime


class OfficeMovement:
    __slots__ = ('id', 'datetime', 'at_workplace', 'room_number')

    def __init__(self, id, datetime_str, at_workplace, room_number):
        self.id = id
        self.datetime = datetime_str
        self.at_workplace = at_workplace
        self.room_number = room_number

    def __setattr__(self, name, value):
        if name == 'id':
            if not isinstance(value, int) or value < 0:
                raise ValueError("id должен быть положительным целым.")
        elif name == 'datetime':
            if not isinstance(value, str):
                raise ValueError("datetime должен быть строкой.")
            try:
                datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                raise ValueError("datetime должен быть в формате ГГГГ-ММ-ДД ЧЧ:ММ:СС")
        elif name == 'at_workplace':
            if not isinstance(value, bool):
                raise ValueError("at_workplace должен быть булевым значением.")
        elif name == 'room_number':
            if not isinstance(value, int) or value < 0:
                raise ValueError("room_number должен быть целым положительным числом.")
        else:
            raise AttributeError(f"Недопустимый атрибут: {name}")
        super().__setattr__(name, value)

    def __repr__(self):
        return f"OfficeMovement(id={self.id}, datetime='{self.datetime}', at_workplace={self.at_workplace}, room_number={self.room_number})"

    def __str__(self):
        return f"№{self.id:<4} {self.datetime:<20} {'Да' if self.at_workplace else 'Нет':<8} Комн. {self.room_number}"


class MovementCollection:

    def __init__(self, records=None):
        self._records = list(records) if records else []

    def add(self, movement):
        if not isinstance(movement, OfficeMovement):
            raise TypeError("Требуется объект OfficeMovement")
        self._records.append(movement)

    def __iter__(self):
        return iter(self._records)

    def __getitem__(self, index):
        return self._records[index]

    def __len__(self):
        return len(self._records)

    def __repr__(self):
        return f"MovementCollection({self._records})"

    @staticmethod
    def validate_datetime(datetime_str):
        try:
            datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
            return True
        except ValueError:
            return False

    @staticmethod
    def str_to_bool(s):
        return s.strip().lower() in ('true', 'да', 'yes', 'y', '1')

    def filter_by_workplace(self, at_workplace=True):
        for m in self._records:
            if m.at_workplace == at_workplace:
                yield m

    def sorted_by_datetime(self):
        for m in sorted(self._records, key=lambda x: x.datetime):
            yield m

    def sorted_by_id(self):
        for m in sorted(self._records, key=lambda x: x.id):
            yield m


class FilteredCollection(MovementCollection):
    def __init__(self, records, filter_key='at_workplace', filter_value=True):
        filtered = [r for r in records if getattr(r, filter_key, None) == filter_value]
        super().__init__(filtered)


def load_from_csv(filepath):
    """Загрузка коллекции из CSV-файла. Статический метод класса? Нет, вынесен отдельно."""
    collection = MovementCollection()
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                movement = OfficeMovement(
                    id=int(row['id']),
                    datetime_str=row['datetime'],
                    at_workplace=MovementCollection.str_to_bool(row['at_workplace']),
                    room_number=int(row['room_number'])
                )
                collection.add(movement)
    except FileNotFoundError:
        print(f"Файл {filepath} не найден. Будет создана пустая коллекция.")
    return collection


def save_to_csv(collection, filepath):
    """Сохранение коллекции в CSV."""
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'datetime', 'at_workplace', 'room_number'])
        writer.writeheader()
        for m in collection:
            writer.writerow({
                'id': m.id,
                'datetime': m.datetime,
                'at_workplace': 'True' if m.at_workplace else 'False',
                'room_number': m.room_number
            })


def main():
    print("Лабораторная работа №4. Вариант 17. История перемещений офисных работников.\n")

    csv_file = "data.csv"
    if not os.path.isfile(csv_file):
        sample_collection = MovementCollection()
        sample_data = [
            OfficeMovement(1, "2025-04-01 09:15:00", True, 101),
            OfficeMovement(2, "2025-04-01 10:30:00", False, 202),
            OfficeMovement(3, "2025-04-01 08:45:00", True, 101),
            OfficeMovement(4, "2025-04-02 11:00:00", True, 303),
            OfficeMovement(5, "2025-04-02 09:00:00", False, 404),
        ]
        for m in sample_data:
            sample_collection.add(m)
        save_to_csv(sample_collection, csv_file)
        print(f"Создан пример файла {csv_file}")

    collection = load_from_csv(csv_file)
    print(f"Загружено записей: {len(collection)}\n")

    print("=== Итерация по коллекции ===")
    for movement in collection:
        print(movement)

    print("\n=== Доступ по индексу ===")
    print("Первый элемент:", collection[0])

    print("\n=== repr коллекции ===")
    print(repr(collection))

    print("\n=== Генератор: записи на рабочем месте ===")
    for m in collection.filter_by_workplace(True):
        print(m)

    print("\n=== Генератор: сортировка по дате ===")
    for m in collection.sorted_by_datetime():
        print(m)

    print("\n=== Статические методы ===")
    dt = "2025-05-08 12:00:00"
    print(f"Дата '{dt}' валидна? {MovementCollection.validate_datetime(dt)}")
    print(f"Строка 'True' в bool: {MovementCollection.str_to_bool('True')}")

    print("\n=== Наследование: FilteredCollection (только на рабочем месте) ===")
    fc = FilteredCollection(list(collection), 'at_workplace', True)
    for m in fc:
        print(m)

    print("\n=== Добавление новой записи ===")
    try:
        new_movement = OfficeMovement(
            id=6,
            datetime_str="2025-05-08 14:30:00",
            at_workplace=True,
            room_number=500
        )
        collection.add(new_movement)
        save_to_csv(collection, csv_file)
        print("Запись добавлена успешно.")
    except Exception as e:
        print(f"Ошибка при добавлении: {e}")


if __name__ == "__main__":
    main()