import hashlib


class CardParametrs:
    """
    A class for checking credit card numbers for hash matching
    """

    def __init__(self, hash_str: str, last_numbers: str, bins: list) -> None:
        """
        Initializes the attributes of class.

        param:
        hash_str (str): A hash string for comparing hashes of card numbers.
        last_numbers (str): The last digits of the card number.
        bin (list): A list of bins for generating card numbers.
        """
        self.hash_str = hash_str
        self.last_numbers = last_numbers
        self.bins_list = bins

    def number_check(self, middle_number: str) -> str:
        """
        Checks the card number with the specified number to match the hash.

        param:
        middle_number (str): The number to generate the card number.
        return:
        str: The card number corresponding to the hash, if found, else None.
        """
        middle_number = int(middle_number)
        for bin in self.bins_list:
            card_number = f"{bin}{middle_number:06d}{self.last_numbers}"
            if hashlib.sha224(card_number.encode()).hexdigest() == self.hash_str:
                return card_number
        return None
