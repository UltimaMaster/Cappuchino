import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class MainWindowCoffee(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.addButton.clicked.connect(self.add_coffee)
        self.saveButton.clicked.connect(self.save_to_db)
        self.select_data()
        self.tableWidget.cellChanged['int', 'int'].connect(self.check_change)

    def select_data(self):
        # Подключаемся к базе
        connection = sqlite3.connect("coffee.sqlite")
        # Делаем запрос и получаем данные
        query = "SELECT * FROM coffee"
        res = connection.cursor().execute(query).fetchall()
        
        # Заполним размеры таблицы
        row, col = len(res), len(res[0]) - 1
        self.tableWidget.setColumnCount(col)
        self.tableWidget.setRowCount(row)
        self.tableWidget.setHorizontalHeaderLabels(["Название", "Обжарка", "Тип", "Вкус", "Цена", "Объем"])
        # Заполняем таблицу элементами
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            # Игнорируем данные id
            for j, elem in enumerate(row[1:]):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        connection.close()
    
    # Открывает диалоговое окно для создания новой записи
    def add_coffee(self):
        coffee_dialog = CoffeeDialog()
        coffee_dialog.show()
        coffee_dialog.exec()
        # Обновляем данные таблицы
        self.select_data()
    
    # Не доделана
    def save_to_db(self):
        connection = sqlite3.connect('coffee.sqlite')
        
        query = "SELECT * FROM coffee"
        res = connection.cursor().execute(query).fetchall()
        row_value, col_value = len(res), len(res[0]) - 1
        
        cur = connection.cursor()
        # Очищаем базу
        cur.execute('DELETE FROM coffee')
        connection.commit()

        # Заполняем базу значениями из таблицы
        for i in range(row_value):
            row_data = [self.tableWidget.item(i, j).text() for j in range(col_value)]
            print(row_data)
            cur.execute('INSERT INTO coffee(Name, Roasting, Type, Taste, Price, Size) VALUES (?,?,?,?,?,?)',
                        [row_data[0], row_data[1], row_data[2], row_data[3], row_data[4], row_data[5]])
        connection.commit()
        connection.close()
    
    # Хотелось добавить возможность редактирования ячеек таблицы и с последующим изменением в базе данных
    def check_change(self):
        row_value = self.tableWidget.currentItem().row()
        col_value = self.tableWidget.currentItem().column()

        print(row_value)
        print(col_value)
        
        value = self.tableWidget.currentItem().text()
        
        colomn_head = ['Name', 'Roasting', 'Type', 'Taste', 'Price', 'Size']
        connection = sqlite3.connect('coffee.sqlite')
        
        print(colomn_head[int(col_value)])
        
        query = 'UPDATE coffee SET ' + colomn_head[int(col_value)] + ' = ' + value + ' WHERE ID = ' + str(row_value)
        
        print(query)
        
        connection.cursor().execute(query)
        connection.commit()
        connection.close()
        print(self.tableWidget.currentItem().row())
        
        
class CoffeeDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("addEditCoffeeForm.ui", self)
    
    # Добавляет запись в базу
    def accept(self):
        connection = sqlite3.connect('coffee.sqlite')
        cur = connection.cursor()
        cur.execute('INSERT INTO coffee(Name, Roasting, Type, Taste, Price, Size) VALUES (?,?,?,?,?,?)',
                    [self.NameLineEdit.text(), self.RoastingLineEdit.text(), self.TypeLineEdit.text(),
                     self.TasteLineEdit.text(), self.PriceLineEdit.text(), self.SizeLineEdit.text()])
        connection.commit()
        connection.close()
        self.done(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindowCoffee()
    ex.show()
    sys.exit(app.exec())
