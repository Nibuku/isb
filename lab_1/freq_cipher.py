import os
import logging
from open_save_part import open_file, write_data, dict_save


logging.basicConfig(level=logging.INFO)


def get_dict(path: str, new_path: str) -> dict:
    data = open_file(path)
    my_dict = dict()
    for i in data:
        my_dict[i] = round((data.count(i) / len(data)), 5)
    sorted_dict = dict(sorted(my_dict.items(), key=lambda x: x[1], reverse=True))
    dict_save(
        sorted_dict, new_path, "Частотный анализ символов в закодированном тексте\n"
    )
    return sorted_dict


def decoding(old: str, new: str, data: str, path_for_dict: str, dict: dict) -> str:
    data = data.replace(old, new)
    dict[old] = new
    dict_save(dict, path_for_dict, "Ключ\n")
    return data


if __name__ == "__main__":

    dictionary = get_dict(
        os.path.join("lab_1", "task2", "code4.txt"),
        os.path.join("lab_1", "task2", "freq.txt"),
    )

    key = dict()
    data = open_file(os.path.join("lab_1", "task2", "code4.txt"))
    data = decoding("М", "*", data, os.path.join("lab_1", "task2", "keys.txt"), key)
    data = decoding("Х", "н", data, os.path.join("lab_1", "task2", "keys.txt"), key)
    data = decoding("4", "а", data, os.path.join("lab_1", "task2", "keys.txt"), key)
    data = decoding("У", "л", data, os.path.join("lab_1", "task2", "keys.txt"), key)
    data = decoding(" ", "и", data, os.path.join("lab_1", "task2", "keys.txt"), key)
    data = decoding("R", "т", data, os.path.join("lab_1", "task2", "keys.txt"), key)
    data = decoding("7", "й", data, os.path.join("lab_1", "task2", "keys.txt"), key)
    data = decoding("1", "о", data, os.path.join("lab_1", "task2", "keys.txt"), key)
    data = decoding("Е", "с", data, os.path.join("lab_1", "task2", "keys.txt"), key)
    data = decoding("B", "г", data, os.path.join("lab_1", "task2", "keys.txt"), key)
    data = decoding("Д", "р", data, os.path.join("lab_1", "task2", "keys.txt"), key)
    data = decoding("Ф", "м", data, os.path.join("lab_1", "task2", "keys.txt"), key)
    data = decoding("A", "в", data, os.path.join("lab_1", "task2", "keys.txt"), key)
    data = decoding("Р", "з", data, os.path.join("lab_1", "task2", "keys.txt"), key)
    data = decoding("8", "к", data, os.path.join("lab_1", "task2", "keys.txt"), key)
    data = decoding("А", "ь", data, os.path.join("lab_1", "task2", "keys.txt"), key)
    data = decoding("О", "е", data, os.path.join("lab_1", "task2", "keys.txt"), key)
    data = decoding("2", "п", data, os.path.join("lab_1", "task2", "keys.txt"), key)
    data = decoding("5", "б", data, os.path.join("lab_1", "task2", "keys.txt"), key)
    data = decoding("C", "д", data, os.path.join("lab_1", "task2", "keys.txt"), key)
    data = decoding("Л", "я", data, os.path.join("lab_1", "task2", "keys.txt"), key)
    data = decoding("Ы", "ш", data, os.path.join("lab_1", "task2", "keys.txt"), key)
    data = decoding("Й", "х", data, os.path.join("lab_1", "task2", "keys.txt"), key)
    data = decoding("П", "ж", data, os.path.join("lab_1", "task2", "keys.txt"), key)
    data = decoding("К", "ю", data, os.path.join("lab_1", "task2", "keys.txt"), key)
    data = decoding("Ь", "щ", data, os.path.join("lab_1", "task2", "keys.txt"), key)
    data = decoding("T", "у", data, os.path.join("lab_1", "task2", "keys.txt"), key)
    data = decoding("Б", "э", data, os.path.join("lab_1", "task2", "keys.txt"), key)
    data = decoding("И", "ф", data, os.path.join("lab_1", "task2", "keys.txt"), key)
    data = decoding("*", " ", data, os.path.join("lab_1", "task2", "keys.txt"), key)
    data = decoding(">", "и", data, os.path.join("lab_1", "task2", "keys.txt"), key)
    data = decoding("Ч", "ц", data, os.path.join("lab_1", "task2", "keys.txt"), key)
    write_data(os.path.join("lab_1", "task2", "decoding_text.txt"), data)
