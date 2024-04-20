import logging
import os
import hashlib
import json

logging.basicConfig(level=logging.INFO)


class CardParametrs:
    def __init__(self, save_path: str, hash_str: str, last_numbers: str, bins: list):
        self.hash_str = hash_str
        self.last_numbers = last_numbers
        self.bins_list = bins
        self.save_path = save_path

    def number_check(self, middle_number: str) -> str:
        middle_number = int(middle_number)
        for bin in self.bins_list:
            card_number = f"{bin}{middle_number:06d}{self.last_numbers}"
            if hashlib.sha224(card_number.encode()).hexdigest() == self.hash_str:
                logging.info(f"Номер карты: {card_number} - найден")
                try:
                    with open(self.save_path, "a", encoding="utf-8") as fp:
                        json.dump({"card_numbers": card_number}, fp)
                except Exception as ex:
                    logging.error(f"Failed to save dictionary: {ex}\n")
            logging.info(f"Номер карты: {card_number} - не соответствует хешу")
        return " "
