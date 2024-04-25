import sys
import logging

from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import (
    QLineEdit,
    QApplication,
    QMainWindow,
    QPushButton,
    QMessageBox,
    QHBoxLayout,
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

        self.setGeometry(500, 50, 600, 500)
        self.setAutoFillBackground(True)
        main_widget = QWidget()
        button_layout = QVBoxLayout()
        data_layout = QHBoxLayout()
        layout = QGridLayout()

        self.setWindowTitle("Поиск и проверка номера карты по хэшу")

        self.btn_bins = QLineEdit(placeholderText="Введите список BIN-ов")
        self.btn_hash_card = QLineEdit(placeholderText="Введите хэш")
        self.btn_last_number = QLineEdit(placeholderText="Введите последние 4 цифры")

        # кнопки
        self.btn_number_search = self.add_button("Найти номер карты по хэшу", 250, 40)
        self.btn_luna = self.add_button("Проверить номер по алгоритму Луна", 250, 40)
        self.btn_graph = self.add_button("Построить граф", 250, 40)
        self.go_to_exit = self.add_button("Выйти из программы", 150, 40)

        self.btn_number_search.clicked.connect(self.check)
        self.btn_luna.clicked.connect(self.luna_alg)
        self.btn_graph.clicked.connect(self.graph_draw)

        # делаем виджеты адаптивными под размер окна
        data_layout.addWidget(self.btn_bins)
        data_layout.addWidget(self.btn_hash_card)
        data_layout.addWidget(self.btn_last_number)
        button_layout.addWidget(self.btn_number_search)
        button_layout.addWidget(self.btn_luna)
        button_layout.addWidget(self.btn_graph)
        button_layout.addWidget(self.go_to_exit)
        layout.addLayout(data_layout, 1, 0)
        layout.addLayout(button_layout, 0, 0)
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

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

    def check(self) -> None:
        """
        Function uses the data entered by the user
        and calls the function of matching the card number by hash
        """
        try:
            bins = self.btn_bins.text().split(",")
            hash_card = self.btn_hash_card.text()
            last_number = self.btn_last_number.text()
            directory = QFileDialog.getSaveFileName(
                self,
                "Выберите файл для сохранения найденного номера:",
                "",
                "JSON File(*.json)",
            )[0]
            if (
                (bins == [])
                or (hash_card == "")
                or (last_number == "")
                or (directory == "")
            ):
                QMessageBox.information(
                    self,
                    "Внимание!",
                    "Были указаны не все данные карты для поиска номера",
                )
            fp.number_selection(
                directory,
                hash_card,
                int(last_number),
                [int(item) for item in bins],
            )
            QMessageBox.information(None, "Успешно", f"Номер карты найдет")
        except Exception as ex:
            logging.error(f"The card number was not found: {ex.args}\n")

    def luna_alg(self) -> None:
        """
        Function calls the function of
        checking card number using the Moon algorithm
        """
        try:
            card_number = QInputDialog.getText(
                self, "Введите номер карты", "Номер карты:"
            )
            card_number = card_number[0]
            if card_number == "":
                QMessageBox.information(
                    None, "Введите номер карты!", "Номер карты не был введен."
                )
            result = fp.luna(card_number)
            QMessageBox.information(
                None, "Результат проверки", f"Номер карты действителен: {result}"
            )
        except Exception as ex:
            logging.error(f"Error during card number verification: {ex.args}\n")

    def graph_draw(self) -> None:
        """
        Function calls the function of plotting
        time dependence on number of processes
        """
        try:
            bins = self.btn_bins.text().split(",")
            hash_card = self.btn_hash_card.text()
            last_number = self.btn_last_number.text()
            if (bins == "") or (hash_card == "") or (last_number == ""):
                QMessageBox.information(
                    None,
                    "Были указаны не все данные карты",
                    "Пожалуйста, заполните все данные карты.",
                )
            fp.graph(hash_card, int(last_number), [int(item) for item in bins])
            QMessageBox.information(None, "Успешно", "График построен")
        except Exception as ex:
            logging.error(f"Error during graph creation: {ex.args}\n")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()
