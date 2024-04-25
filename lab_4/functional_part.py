import json
import logging
import matplotlib.pyplot as plt
import multiprocessing as mp
import time

from class_card import CardParametrs

logging.basicConfig(level=logging.INFO)


def number_selection(
    save_path: str, hash_str: str, last_numbers: str, bins: list
) -> None:
    """
    Search for credit card numbers, by hash, and save them to a file.
    The function uses multiple processes to reduce the search time.

    param:
        save_path (str): The path to save the file.
        hash_str (str): A hash string for hashes of card numbers.
        last_numbers (str): The last digits of the card number.
        bin (list): A list of bins ) for generating card numbers.
    """
    found_numbers = list()
    my_card = CardParametrs(hash_str, last_numbers, bins)
    with mp.Pool(mp.cpu_count()) as p:
        results = p.starmap(my_card.number_check, [(i,) for i in range(0, 999999)])
        for result in results:
            if result is not None:
                found_numbers.append(result)
    try:
        with open(save_path, "w", encoding="utf-8") as fp:
            json.dump({"card_numbers": found_numbers}, fp)
    except Exception as ex:
        logging.error(f"Failed to save dictionary: {ex}\n")


def luna(card_number: str) -> bool:
    """
    Checking the credit card number using the Moon algorithm.

    param:
    card_number (str): The credit card number.
    return:
    bool: The result of the check
    """
    check = int(card_number[-1])
    card_number = [int(i) for i in card_number]
    for i in range(1, len(card_number), 2):
        card_number[i] *= 2
        if card_number[i] > 9:
            card_number[i] = (card_number[i] // 10) + (card_number[i] % 10)
    total_sum = sum(card_number)
    check_sum = (10 - (total_sum % 10)) % 10
    return check_sum == check


def graph(hash_str: str, last_numbers: str, bins: list) -> None:
    """
    Creating a graph of time dependence on the number of processes when searching for card numbers.

    param:
    hash_str (str): Hash for comparing hash numbers of cards.
    last_numbers (str): The last digits of the card number.
    bin (list): A list of BIN's for generating card numbers.
    """
    times = []
    my_card = CardParametrs(hash_str, last_numbers, bins)
    for i in range(1, int(mp.cpu_count() * 1.5)):
        start = time.time()
        with mp.Pool(i) as p:
            for i, result in enumerate(
                p.starmap(my_card.number_check, [(i,) for i in range(0, 999999)])
            ):
                if result:
                    end = time.time() - start
                    times.append(end)
                    break
    plt.plot(range(len(times)), times)
    plt.plot(range(len(times)), times)
    plt.plot(
        range(len(times)),
        times,
        color="pink",
        marker="o",
        markersize=7,
    )
    plt.bar(range(len(times)), times, alpha=0.5)
    plt.xlabel("Количество процессов")
    plt.ylabel("Затраченное время в секундах")
    plt.title("График зависимости времени от числа процессов")
    plt.show()
