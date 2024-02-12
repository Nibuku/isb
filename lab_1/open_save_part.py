import re
import json
import logging


logging.basicConfig(level=logging.INFO)


def open_file(path: str) -> str:
    "Function for open .txt-files and making str"
    try:
        with open(path, "r+", encoding="utf-8") as file:
            data = file.read()
        return data
    except:
        logging.error("Failed to open file or file was not found")


def write_data(path: str, data: str) -> None:
    """Function for write str-dats in .txt-file"""
    try:
        with open(path, "w", encoding="utf-8") as file:
            file.write(data)
    except:
        logging.error("Failed to write data or file was not found")


def formatting(path: str) -> None:
    """Function for formatting text:
    removes punctuation marks and results in uppercase"""
    try:
        data = open_file(path)
        new_text = str.upper(data)
        clean_string = re.sub("\W+", " ", new_text)
        write_data(path, clean_string)
    except:
        logging.error("Failed to formatting data")


def dict_save(dictionary: dict, path: str) -> None:
    """saving a dictionary to a file with a given message"""
    try:
        with open(path, "w", encoding="utf-8") as fp:
            json.dump(dictionary, fp, ensure_ascii=False, indent=1)
    except:
        logging.error("Failed to saving dictionary")
