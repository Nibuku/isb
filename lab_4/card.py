import multiprocessing as mp
import logging
import json
import os
import time
import matplotlib.pyplot as plt
from functional_part import CardParametrs

logging.basicConfig(level=logging.INFO)


def number_selection(
    save_path: str, hash_str: str, last_numbers: str, bins: list, pool_count: float
):
    found_numbers = list()
    my_card = CardParametrs(hash_str, last_numbers, bins)
    with mp.Pool(int(mp.cpu_count() * pool_count)) as p:
        results = p.starmap(my_card.number_check, [(i,) for i in range(0, 999999)])
        for result in results:
            if result is not None:
                found_numbers.append(result)
    try:
        with open(save_path, "a", encoding="utf-8") as fp:
            json.dump({"card_numbers": found_numbers}, fp)
    except Exception as ex:
        logging.error(f"Failed to save dictionary: {ex}\n")


def luna(card_number: str) -> bool:
    check = int(card_number[-1])
    card_number = [int(i) for i in card_number]
    for i in range(1, len(card_number), 2):
        card_number[i] *= 2
        if card_number[i] > 9:
            card_number[i] = (card_number[i] // 10) + (card_number[i] % 10)
    total_sum = sum(card_number)
    check_sum = (10 - (total_sum % 10)) % 10
    return check_sum == check


def graph(
    save_path: str, hash_str: str, last_numbers: str, bins: list, pool_count: float
):
    pool_counts = [i for i in range(1, int(mp.cpu_count() * pool_count), 2)]
    times = list()
    for i in range(1, int(mp.cpu_count() * pool_count), 2):
        start = time.time()
        number_selection(save_path, hash_str, last_numbers, bins, i)
        end = time.time() - start
        times.append(end / 60)
    plt.plot(pool_counts, time)
    plt.plot(pool_counts, time, color="rose", marker="o", markersize=7)
    plt.bar(pool_counts, time, alpha=0.5)
    plt.xlabel("Количество процессов")
    plt.ylabel("Затраченное время в минутах")
    plt.title("График зависимости времени от числа процессов")
    plt.show()


if __name__ == "__main__":
    with open(os.path.join("lab_4", "constance.json"), "r") as file:
        const = json.load(file)
    number_selection("lab_4/card_number.json", const["HASH"], "1217", const["BINS"], 1)
