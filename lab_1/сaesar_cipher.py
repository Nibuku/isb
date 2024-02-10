import os
import re
import logging


logging.basicConfig(level=logging.INFO)

RUS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"


def open_file(path: str) -> str:
    with open(path, "r+", encoding="utf-8") as file:
        data = file.read()
    return data


def write_data(path: str, data: str) -> None:
    text_file = open(path, "w", encoding="utf-8")
    text_file.write(data)
    text_file.close()


def formatting(path: str) -> None:
    try:
        data = open_file(path)
        new_text = str.upper(data)
        clean_string = re.sub("\W+", " ", new_text)
        write_data(path, clean_string)
    except:
        logging.error(f"Failed to write data\n")


def codding(path: str, new_path: str, step: int) -> None:
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


def decodding(path: str, new_path: str, step: int) -> None:
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


if __name__ == "__main__":

    codding(
        os.path.join("lab_1", "task1_text_one.txt"),
        os.path.join("lab_1", "task1_text_two.txt"),
        3,
    )
    decodding(
        os.path.join("lab_1", "task1_text_two.txt"),
        os.path.join("lab_1", "task1_text_three.txt"),
        3,
    )
