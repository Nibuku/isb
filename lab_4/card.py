import multiprocessing as mp
import logging
import json
import os
from functional_part import CardParametrs

logging.basicConfig(level=logging.INFO)


def number_selection(save_path: str, hash_str: str, last_numbers: str, bins: list):
    my_card = CardParametrs(save_path, hash_str, last_numbers, bins)
    with mp.Pool(mp.cpu_count()) as p:
        p.starmap(my_card.number_check, [(i,) for i in range(0, 999999)])


if __name__ == "__main__":
    with open(os.path.join("lab_4", "constance.json"), "r") as file:
        const = json.load(file)
    number_selection("lab_4/card_number.json", const["HASH"], "1217", const["BINS"])
