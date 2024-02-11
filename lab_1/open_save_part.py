import re
import logging


logging.basicConfig(level=logging.INFO)


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
        logging.error(f"Failed to formatting data\n")


def dict_save(dict: dict, path: str, message: str) -> None:
    with open(path, "w", encoding="utf-16") as convert_file:
        convert_file.write(f"{message}\n")
        for key, value in dict.items():
            convert_file.write(f"{key}:{value}\n")
