import sys
import logging

from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import (
    QLineEdit,
    QApplication,
    QMainWindow,
    QPushButton,
    QMessageBox,
    QComboBox,
    QFileDialog,
    QVBoxLayout,
    QWidget,
    QGridLayout,
    QInputDialog,
)

import functional_part as fp

logging.basicConfig(level=logging.INFO)


class MainWindow(QMainWindow):

    def __init__(self) -> None:
        """Initialize the main window with buttons and layouts"""
        super().__init__()

        self.setGeometry(400, 100, 500, 500)
        main_widget = QWidget()
        button_layout = QVBoxLayout()
        layout = QGridLayout()

        self.setWindowTitle("Поиск и проверка номера карты по хэшу")

        self.btn_bins = QLineEdit(placeholderText="Введите список BIN-ов")
        self.btn_hash_card = QLineEdit(placeholderText="Введите хэш")
        self.btn_last_number = QLineEdit(placeholderText="Введите последние 4 цифры")

        self.bins = self.btn_bins.text().split(",")
        self.hash_card = self.btn_hash_card.text()
        self.last_number = self.btn_last_number.text()
        # self.textbox.move(20, 20)
        # self.textbox.resize(280, 40)

        # кнопки
        self.btn_number_search = self.add_button("Найти номер карты по хэшу", 250, 40)
        self.btn_luna = self.add_button("Проверить номер по алгоритму Луна", 250, 40)
        self.btn_graph = self.add_button("Построить граф", 250, 40)
        self.go_to_exit = self.add_button("Выйти из программы", 150, 40)

        # делаем виджеты адаптивными под размер окна
        button_layout.addWidget(self.btn_bins)
        button_layout.addWidget(self.btn_hash_card)
        button_layout.addWidget(self.btn_last_number)
        button_layout.addWidget(self.btn_number_search)
        button_layout.addWidget(self.btn_luna)
        button_layout.addWidget(self.btn_graph)
        button_layout.addWidget(self.go_to_exit)
        layout.addLayout(button_layout, 0, 1)
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        self.btn_number_search.clicked.connect(self.check)
        self.btn_luna.clicked.connect(self.luna_alg)
        self.btn_graph.clicked.connect(self.graph_draw)

        self.show()

    def add_button(self, name: str, size_x: int, size_y: int) -> QPushButton:
        """The function creates buttons with the specified names and sizes
        parametrs:
        name: the name of the button;
        size_x: size by x;
        size_y: size by y
        return QPushButton"""
        button = QPushButton(name, self)
        button.resize(button.sizeHint())
        button.setFixedSize(QSize(size_x, size_y))
        return button

    def check(self):
        try:
            directory = QFileDialog.getSaveFileName(
                self,
                "Выберите файл для сохранения найденного номера:",
                "",
                "JSON File(*.json)",
            )[0]
            if (
                (self.bins == [])
                or (self.hash_card == "")
                or (self.last_number == "")
                or (directory == "")
            ):
                QMessageBox.information(
                    self,
                    "Были указаны не все данные карты для поиска номера",
                    "Внимание!",
                    QMessageBox.StandardButton.Ok,
                )
                return
            result = fp.number_selection(
                directory,
                self.hash_card,
                int(self.last_number),
                [int(item) for item in self.bins],
            )
            QMessageBox.information(None, "Успешно", f"Номер карты найдет:{result}")
        except Exception as ex:
            logging.error(f"Couldn't generation keys: {ex.args}\n")

    def luna_alg(self):
        try:
            card_number = QInputDialog.getText(
                self, "Введите номер карты", "Номер карты:"
            )
            if card_number.text() == "":
                QMessageBox.information(
                    None, "Введите номер карты!", "Пожалуйста, введите номер карты."
                )
                return
            result = fp.luna(card_number)
            QMessageBox.information(
                None, "Результат проверки", f"Номер карты действителен: {result}"
            )
        except Exception as ex:
            logging.error(f"Couldn't generation keys: {ex.args}\n")

    def graph_draw(self):
        try:
            if (self.bins == "") or (self.hash_card == "") or (self.last_number == ""):
                QMessageBox.information(
                    None,
                    "Были указаны не все данные карты",
                    "Пожалуйста, заполните все данные карты.",
                )
                return
            fp.graph(
                self.hash_card, int(self.last_number), [int(item) for item in self.bins]
            )
            QMessageBox.information(None, "Успешно", "Граф построен")
        except Exception as ex:
            logging.error(f"Couldn't generation keys: {ex.args}\n")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()
