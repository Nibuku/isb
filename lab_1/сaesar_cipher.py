import os
import logging
from open_save_part import open_file, write_data, dict_save

logging.basicConfig(level=logging.INFO)

RUS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"


def codding(path: str, new_path: str, step: int) -> None:
    """Function takes path to the file to be encrypted,
    second path is path for save, and step with which
    the text will be encoded using the caesar cipher"""
    try:
        data = open_file(path)
        codding_str = ""
        for i in data:
            if i == " ":
                codding_str += i
                continue
            index = RUS.find(i)
            new_index = (index + step) % len(RUS)
            codding_str += RUS[new_index]
        write_data(new_path, codding_str)
    except:
        logging.error(f"The symbol was not found\n")


def key_dict(path: str, step: int, message) -> None:
    """Function creates a dictionary-key for the Caesar cipher with a given step"""
    key = dict()
    for i in RUS:
        index = RUS.find(i)
        key[i] = RUS[(index + step) % len(RUS)]
    dict_save(key, path, message)


def decodding(path: str, new_path: str, step: int) -> None:
    """Function takes path to the file to be decrypted,
    second path is path for save, and step with which
    the text will be decoded using the caesar cipher"""
    try:
        data = open_file(path)
        codding_str = ""
        for i in data:
            if i == " ":
                codding_str += i
                continue
            index = RUS.find(i)
            new_index = (index - step) % len(RUS)
            codding_str += RUS[new_index]
        write_data(new_path, codding_str)
    except:
        logging.error(f"The symbol was not found\n")


if __name__ == "__main__":

    codding(
        os.path.join("lab_1", "task1", "base_text.txt"),
        os.path.join("lab_1", "task1", "encoded_text.txt"),
        3,
    )
    key_dict(os.path.join("lab_1", "task1", "key.txt"), 3, "Ключ к шифру Цезаря")
    decodding(
        os.path.join("lab_1", "task1", "encoded_text.txt"),
        os.path.join("lab_1", "task1", "decoded_text.txt"),
        3,
    )
