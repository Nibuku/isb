import os
import re
import json
import logging
from сaesar_cipher import open_file, write_data


logging.basicConfig(level=logging.INFO)

FREQ = " ОИЕАНТСРВМЛДЯКПЗЫЬУЧЖГХФЙЮБЦШЩЭЪ"


def get_dict(path: str, new_path) -> dict:
    data = open_file(path)
    my_dict = dict()
    for i in data:
        my_dict[i] = round((data.count(i) / len(data)), 5)
    sorted_dict = dict(sorted(my_dict.items(), key=lambda x: x[1], reverse=True))
    with open(new_path, "w", encoding="utf-16") as convert_file:
        convert_file.write("Частотный анализ символов в закодированном тексте\n")
        for key, value in sorted_dict.items():
            convert_file.write(f"{key}:{value}\n")
    return sorted_dict


if __name__ == "__main__":

    dictionary = get_dict(
        os.path.join("lab_1", "task2_one.txt"), os.path.join("lab_1", "task2_key.txt")
    )
    print(dictionary)

    # my_dict = dict(enumerate(FREQ, start=1))
    # freq_dict = dict(zip(my_dict.values(), my_dict.keys()))
    # first_key = dict(zip(dictionary.keys(), freq_dict.keys()))
    key = dict()
    data = open_file(os.path.join("lab_1", "task2_one.txt"))
    data = data.replace("М", "*")
    key["М"] = " "
    data = data.replace("Х", "н")
    key["X"] = "н"
    data = data.replace("4", "а")
    key["4"] = "a"
    data = data.replace("У", "л")
    data = data.replace(" ", "и")
    data = data.replace("R", "т")
    data = data.replace("7", "й")
    data = data.replace("1", "о")
    data = data.replace("Е", "с")
    data = data.replace("B", "г")
    data = data.replace("Д", "р")
    data = data.replace("Ф", "м")
    data = data.replace("A", "в")
    data = data.replace("Р", "з")
    data = data.replace("8", "к")
    data = data.replace("А", "ь")
    data = data.replace("О", "е")
    data = data.replace("2", "п")
    data = data.replace("5", "б")
    data = data.replace("C", "д")
    data = data.replace("Л", "я")
    data = data.replace("Ы", "ш")
    data = data.replace("Й", "х")
    data = data.replace("П", "ж")
    data = data.replace("К", "ю")
    data = data.replace("Ь", "щ")
    data = data.replace("T", "у")
    data = data.replace("Б", "э")
    data = data.replace("И", "ф")
    # data = data.replace("и", "ч")
    print(data)
    # print(key)
    # print(first_key)
