import os
import sys
import logging
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QMessageBox,
    QLabel,
    QLineEdit,
    QComboBox,
    QFileDialog,
    QVBoxLayout,
    QWidget,
    QGridLayout,
)
from PyQt6.QtGui import QPixmap
import cryptography_part as cp

logging.basicConfig(level=logging.INFO)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setGeometry(400, 100, 500, 500)
        self.setWindowTitle("Tooltips")
        main_widget = QWidget()
        button_layout = QVBoxLayout()
        layout = QGridLayout()

        self.setWindowTitle("Шифрование с помощью TripleDes")

        self.dialog = QFileDialog()
        self.dialog.setFileMode(QFileDialog.FileMode.Directory)
        self.symmetric_key_path = self.dialog.getOpenFileName(
            None, "Выберите файл (symmetric)", "", "Text File(*.txt)"
        )[0]
        self.public_key_path = self.dialog.getOpenFileName(
            None, "Выберите файл (public)", "", "Text File(*.pem)"
        )[0]
        self.private_key_path = self.dialog.getOpenFileName(
            None, "Выберите файл (private)", "", "Text File(*.pem)"
        )[0]
        self.key_size = 8

        self.comboBox = QComboBox()
        self.comboBox.addItems(["8", "16", "24"])
        self.comboBox.currentIndexChanged.connect(self.set_key_size)

        # кнопки
        self.btn_generation_key = self.add_button("Сгенерировать ключи", 250, 40)
        self.btn_encryption = self.add_button("Зашифровать текст", 250, 40)
        self.btn_decryption = self.add_button("Расшифровать текст", 250, 40)

        # делаем виджеты адаптивными по размер окна
        button_layout.addWidget(self.comboBox)
        button_layout.addWidget(self.btn_generation_key)
        button_layout.addWidget(self.btn_encryption)
        button_layout.addWidget(self.btn_decryption)

        layout.addLayout(button_layout, 0, 1)

        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        self.cryptography = cp.Cryptograthy(
            self.symmetric_key_path, self.public_key_path, self.private_key_path
        )
        # self.go_to_exit.clicked.connect(self.close)

        self.btn_generation_key.clicked.connect(self.generatoin)
        self.btn_encryption.clicked.connect(self.encryption_text)

        self.show()

    def add_button(self, name: str, size_x: int, size_y: int):
        """The function creates buttons with the specified names and sizes"""
        button = QPushButton(name, self)
        button.resize(button.sizeHint())
        button.setFixedSize(QSize(size_x, size_y))
        return button

    def set_key_size(self):
        self.key_size = int(self.comboBox.currentText())

    def generatoin(self):
        try:
            if (
                (self.symmetric_key_path == "")
                or (self.public_key_path == "")
                or (self.private_key_path == "")
            ):
                QMessageBox.information(
                    None, "Не указан путь", "Не был выбран файл для одного из ключей"
                )
                return
            self.cryptography.key_generation(self.key_size)
            QMessageBox.information(None, "Успешно", "Ключи сгенерированы успешно!")
        except Exception as ex:
            logging.error(f"Couldn't generation keys: {ex.message}\n{ex.args}\n")

    def encryption_text(self):
        base_text, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите путь к файлу с исходным текстом:",
            "",
            "Text File(*.txt)",
        )
        new_file, _ = QFileDialog.getSaveFileName(
            self,
            "Выберите путь сохранения зашифрованного текста:",
            "",
            "Text File(*.txt)",
        )
        try:
            if (not base_text) or (not new_file):
                QMessageBox.information(None, "Не указан путь", "Не был выбран путь")
                return
            self.cryptography.encryption(base_text, new_file)
            QMessageBox.information(None, "Успешно", "Текст зашифрован!")
        except Exception as ex:
            logging.error(f"Couldn't encryption text: {ex}\n")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()
