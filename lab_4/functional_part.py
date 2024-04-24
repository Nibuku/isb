import multiprocessing as mp
import logging
import json
import os
import time
import matplotlib.pyplot as plt
from class_card import CardParametrs

logging.basicConfig(level=logging.INFO)


def number_selection(save_path: str, hash_str: str, last_numbers: str, bins: list):
    found_numbers = list()
    my_card = CardParametrs(hash_str, last_numbers, bins)
    with mp.Pool(mp.cpu_count()) as p:
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


def graph(hash_str: str, last_numbers: str, bins: list):
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


if __name__ == "__main__":
    with open(os.path.join("lab_4", "constance.json"), "r") as file:
        const = json.load(file)
    graph(const["HASH"], "1217", const["BINS"])
