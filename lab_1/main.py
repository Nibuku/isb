import os
import re
import logging


logging.basicConfig(level=logging.INFO)

RUS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"


def formatting(path: str) -> None:
    try:
        with open(path, "r+", encoding="utf-8") as file:  # ignors
            data = file.read()
            new_text = str.upper(data)
            clean_string = re.sub("\W+", " ", new_text)
            file.seek(0)
            file.write(clean_string)
    except:
        logging.error(f"Failed to write data\n")


def codding(path: str, new_path: str, step: int) -> None:
    with open(path, "r+", encoding="utf-8") as file:
        data = file.read()
    codding_str = ""
    for i in data:
        if i == " ":
            codding_str += i
            continue
        index = RUS.find(i)
        new_index = (index + step) % len(RUS)
        codding_str += RUS[new_index]
    text_file = open(new_path, "w", encoding="utf-8")
    text_file.write(codding_str)
    text_file.close()


def decodding(path: str, new_path: str, step: int) -> None:
    with open(path, "r+", encoding="utf-8") as file:
        data = file.read()
    codding_str = ""
    for i in data:
        if i == " ":
            codding_str += i
            continue
        index = RUS.find(i)
        new_index = (index - step) % len(RUS)
        codding_str += RUS[new_index]
    text_file = open(new_path, "w", encoding="utf-8")
    text_file.write(codding_str)
    text_file.close()


if __name__ == "__main__":

    codding(
        os.path.join("lab_1", "text_one.txt"),
        os.path.join("lab_1", "text_two.txt"),
        3,
    )
    decodding(
        os.path.join("lab_1", "text_two.txt"),
        os.path.join("lab_1", "text_three.txt"),
        3,
    )
