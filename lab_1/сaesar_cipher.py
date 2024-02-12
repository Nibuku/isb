import os
import json

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
        logging.error("The symbol was not found")


def key_dict(path: str, step: int) -> None:
    """Function creates a dictionary-key for the Caesar cipher with a given step"""
    key = dict()
    for i in RUS:
        index = RUS.find(i)
        key[i] = RUS[(index + step) % len(RUS)]
    dict_save(key, path)


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

    with open(os.path.join("lab_1", "settings.json"), "r") as file:
        settings = json.load(file)

    codding(
        os.path.join(
            settings["directory"], settings["folder1"], settings["given_text"]
        ),
        os.path.join(settings["directory"], settings["folder1"], settings["coding"]),
        settings["step"],
    )
    key_dict(
        os.path.join(settings["directory"], settings["folder1"], settings["key_file"]),
        settings["step"],
    )
    decodding(
        os.path.join(settings["directory"], settings["folder1"], settings["coding"]),
        os.path.join(settings["directory"], settings["folder1"], settings["decoding"]),
        settings["step"],
    )
