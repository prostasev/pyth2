import csv
import os
from datetime import datetime
from tkinter import Tk
from tabulate import tabulate
from tkinter.filedialog import asksaveasfilename

class AdCampaign:
    def __init__(self, filename):
        self.filename = filename
        self.pending_record = None  # Хранит данные о рекламном ролике, введенные пользователем

    def initialize_db(self):
        """Создает файл, если он не существует, и записывает заголовки, если файл пустой."""
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['ID', 'Заказчик', 'Название ролика', 'Изготовитель', 'Дата', 'Стоимость'])
            print(f"База данных инициализирована: {self.filename}")
        else:
            print(f"База данных инициализирована: {self.filename}")

    def add_record(self, customer, title, manufacturer, date, cost):
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['ID', 'Заказчик', 'Название ролика', 'Изготовитель', 'Дата', 'Стоимость'])
        """Добавляет запись в базу данных."""
        with open(self.filename, 'a', newline='') as file:
            writer = csv.writer(file)
            records = self.read_all()
            record_id = len(records)  # ID начинается с 0
            writer.writerow([record_id, customer, title, manufacturer, date, cost])

    def display_records(self):
        """Выводит все записи в виде таблицы."""
        records = self.read_all()
        headers = ['ID', 'Заказчик', 'Название ролика', 'Изготовитель', 'Дата', 'Стоимость']
        print(tabulate(records[1:], headers=headers, tablefmt='grid', stralign='center'))

    def delete_record(self, index):
        """Удаляет запись по номеру."""
        records = self.read_all()
        if 0 <= index < len(records) - 1:  # -1, чтобы не учитывать заголовок
            del records[index + 1]  # +1, потому что ID начинается с 0
            self.write_all(records)

    def read_all(self):
        """Читает все записи из файла."""
        with open(self.filename, 'r') as file:
            reader = csv.reader(file)
            return list(reader)

    def write_all(self, records):
        """Записывает все записи обратно в файл."""
        with open(self.filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(records)

    def search_by_field(self, field_name, value):
        """Поиск по одному полю."""
        records = self.read_all()
        # Проверка наличия заголовков
        if len(records) == 0:
            print("Нет записей в базе данных.")
            return
        # Проверка, существует ли поле
        try:
            index = records[0].index(field_name)
        except ValueError:
            print(f"Поле '{field_name}' не найдено.")
            return
        # Поиск записей
        results = [record for record in records if record[index] == value]
        self.display_results(results)

    def search_by_two_fields(self, field1, value1, field2, value2):
        """Поиск по двум полям."""
        records = self.read_all()
        index1 = records[0].index(field1)
        index2 = records[0].index(field2)
        results = [record for record in records if record[index1] == value1 and record[index2] == value2]
        self.display_results(results)

    def delete_expired(self):
        """Удаляет все записи с истекшей датой."""
        records = self.read_all()
        current_date = datetime.now().date()
        records = [record for record in records if datetime.strptime(record[4], '%Y-%m-%d').date() >= current_date]
        self.write_all(records)

    def increase_cost(self, customer):
        """Увеличивает стоимость заказа на 10% для заданного заказчика."""
        records = self.read_all()
        for record in records[1:]:
            if record[1] == customer:
                record[5] = str(float(record[5]) * 1.1)
        self.write_all(records)

    def display_results(self, results):
        """Выводит результаты поиска."""
        if not results:
            print("Нет результатов для отображения.")
        else:
            headers = ['ID', 'Заказчик', 'Название ролика', 'Изготовитель', 'Дата', 'Стоимость']
            print(tabulate(results, headers=headers, tablefmt='grid', stralign='center'))

    def display_by_date(self, date):
        """Выводит все сведения о рекламных роликах прокатанных в заданное число."""
        records = self.read_all()

        results = [record for record in records if record[4] == date]

        if not results:
            print(f"Нет записей с датой {date}.")
        else:
            print(tabulate(results, headers=['ID', 'Заказчик', 'Название ролика', 'Изготовитель', 'Дата', 'Стоимость'],
                           tablefmt='grid', stralign='center'))

def choose_file():
    """Открывает диалог для выбора файла."""
    Tk().withdraw()  # Скрывает главное окно Tkinter
    filename = asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    return filename

def main():
    filename = choose_file()
    if not filename:
        print("Файл не выбран. Завершение программы.")
        return

    ad_campaign = AdCampaign(filename)

    while True:
        print("\n1. Инициализировать базу данных")
        print("2. Ввести данные о рекламном ролике")
        print("3. Добавить запись в базу данных")
        print("4. Вывести все записи")
        print("5. Удалить запись по номеру")
        print("6. Поиск по полю")
        print("7. Поиск по двум полям")
        print("8. Удалить записи с истекшей датой")
        print("9. Увеличить стоимость заказа на 10%")
        print("10. Вывести рекламные ролики прокатанные в заданное число")
        print("11. Выход")

        choice = input("Выберите действие: ")

        if choice == '1':
            ad_campaign.initialize_db()  # Инициализация базы данных
        elif choice == '2':
            # Ввод данных о ролике, сохраняем в переменной
            customer = input("Заказчик: ")
            title = input("Название ролика: ")
            manufacturer = input("Изготовитель: ")
            date = input("Дата (YYYY-MM-DD): ")
            cost = input("Стоимость: ")
            ad_campaign.pending_record = (customer, title, manufacturer, date, cost)
            print("Данные о рекламном ролике сохранены.")
        elif choice == '3':
            if ad_campaign.pending_record:
                customer, title, manufacturer, date, cost = ad_campaign.pending_record
                ad_campaign.add_record(customer, title, manufacturer, date, cost)
                print("Запись добавлена.")
                ad_campaign.pending_record = None  # Сбрасываем после добавления
            else:
                print("Нет данных для добавления. Пожалуйста, сначала введите данные.")
        elif choice == '4':
            ad_campaign.display_records()
        elif choice == '5':
            index = int(input("Введите номер записи для удаления: ")) - 1
            ad_campaign.delete_record(index)
            print("Запись удалена.")
        elif choice == '6':
            field = input("Введите поле для поиска: ")
            value = input("Введите значение: ")
            ad_campaign.search_by_field(field, value)
        elif choice == '7':
            field1 = input("Введите первое поле для поиска: ")
            value1 = input("Введите значение для первого поля: ")
            field2 = input("Введите второе поле для поиска: ")
            value2 = input("Введите значение для второго поля: ")
            ad_campaign.search_by_two_fields(field1, value1, field2, value2)
        elif choice == '8':
            ad_campaign.delete_expired()
            print("Истекшие записи удалены.")
        elif choice == '9':
            customer = input("Введите заказчика для увеличения стоимости: ")
            ad_campaign.increase_cost(customer)
            print("Стоимость увеличена.")
        elif choice == '10':
            date = input("Введите дату (YYYY-MM-DD): ")
            ad_campaign.display_by_date(date)
        elif choice == '11':
            break
        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")

if __name__ == "__main__":
    main()

