import re
import logging


logging.basicConfig(level=logging.INFO)


def open_file(path: str) -> str:
    "Function for open .txt-files and making str"
    try:
        with open(path, "r+", encoding="utf-8") as file:
            data = file.read()
        return data
    except:
        logging.error(f"Failed to open file or file was not found\n")


def write_data(path: str, data: str) -> None:
    """Function for write str-dats in .txt-file"""
    try: 
        text_file = open(path, "w", encoding="utf-8")
        text_file.write(data)
        text_file.close()
    except:
        logging.error(f"Failed to write data or file was not found\n")


def formatting(path: str) -> None:
    """Function for formatting text:
    removes punctuation marks and results in uppercase"""
    try:
        data = open_file(path)
        new_text = str.upper(data)
        clean_string = re.sub("\W+", " ", new_text)
        write_data(path, clean_string)
    except:
        logging.error(f"Failed to formatting data\n")


def dict_save(dict: dict, path: str, message: str) -> None:
    """saving a dictionary to a file with a given message"""
    try:
        with open(path, "w", encoding="utf-16") as convert_file:
            convert_file.write(f"{message}\n")
            for key, value in dict.items():
                convert_file.write(f"{key}:{value}\n")
    except: 
        logging.error(f"Failed to saving dictionary\n")
