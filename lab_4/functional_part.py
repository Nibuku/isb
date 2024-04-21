import logging
import os
import hashlib
import json

logging.basicConfig(level=logging.INFO)


class CardParametrs:
    def __init__(self, hash_str: str, last_numbers: str, bins: list):
        self.hash_str = hash_str
        self.last_numbers = last_numbers
        self.bins_list = bins

    def number_check(self, middle_number: str) -> str:
        middle_number = int(middle_number)
        for bin in self.bins_list:
            card_number = f"{bin}{middle_number:06d}{self.last_numbers}"
            if hashlib.sha224(card_number.encode()).hexdigest() == self.hash_str:
                logging.info(f"Номер карты: {card_number} - найден")
                return card_number
        return None
