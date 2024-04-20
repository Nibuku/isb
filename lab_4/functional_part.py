import multiprocessing as mp
import logging
import os
import hashlib
import json

logging.basicConfig(level=logging.INFO)


def number_selection(
    hash: str, last_numbers: str, bins: list, middle_number: str
) -> str:
    # cores = mp.cpu_count()
    for bin in bins:
        card_number = f"{bin}{middle_number}{last_numbers}"
        if hashlib.sha224(card_number.encode()).hexdigest() == hash:
            return card_number
    logging.info(f"Номер карты: {card_number} - не соответствует хешу")
    return False


if __name__ == "__main__":
    with open(os.path.join("lab_4", "constance.json"), "r") as file:
        const = json.load(file)
    print(number_selection(const["HASH"], "1217", const["BINS"], "180243"))
