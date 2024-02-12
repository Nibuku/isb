import os
import json

from open_save_part import open_file, write_data, dict_save


def get_dict(path: str, new_path: str) -> None:
    """Function for doing frequency analysis in the text.
    path: path to the text
    new_path: path for save dict"""
    data = open_file(path)
    my_dict = dict()
    for i in data:
        my_dict[i] = data.count(i) / len(data)
    sorted_dict = dict(sorted(my_dict.items(), key=lambda x: x[1], reverse=True))
    dict_save(sorted_dict, new_path)


def decoding(old: str, new: str, data: str, path_for_dict: str, dict: dict) -> str:
    """Function replaces the specified letters in the text and fixes it in the dictionary
    old: letter to replace
    new: new letter
    data: text
    path_for_dict:path for save dict
    """
    data = data.replace(old, new)
    dict[old] = new
    dict_save(dict, path_for_dict)
    return data


def utility(base_path: str, key_path: str, decoded_path: str) -> None:
    data = open_file(base_path)
    with open(
        key_path,
        "r",
        encoding="utf-8",
    ) as file:
        dictionary = json.load(file)
    for key, value in dictionary.items():
        data = data.replace(key, value)
    data = data.replace("_", " ")
    write_data(decoded_path, data)


if __name__ == "__main__":

    with open(os.path.join("lab_1", "settings.json"), "r") as file:
        settings = json.load(file)

    utility(
        os.path.join(
            settings["directory"], settings["folder2"], settings["original_text"]
        ),
        os.path.join(settings["directory"], settings["folder2"], settings["key_file"]),
        os.path.join(settings["directory"], settings["folder2"], settings["decoding"]),
    )
