import logging
import math
import json
import scipy


logging.basicConfig(level=logging.INFO)


class NistTest:
    def __init__(self, bit_sequence: str) -> None:
        self.sequence = bit_sequence
        self.len = len(bit_sequence)

    def bitwise_test(self) -> bool:
        sum = 0
        for i in self.sequence:
            if int(i) == 1:
                sum += 1
            else:
                sum -= 1
        sum *= 1 / math.sqrt(self.len)
        p_value = math.erf(sum / math.sqrt(2))
        return p_value > 0.01

    def same_bits_test(self) -> bool:
        counter = 0
        for i in self.sequence:
            counter += int(i)
        counter *= 1 / self.len
        if abs(counter - 0.5) < 2 / math.sqrt(self.len):
            v = 0
            for i in range(self.len - 1):
                if float(i) != float(i + 1):
                    v += 1
            num = abs(v - 2 * self.len * counter * (1 - counter))
            denom = 2 * math.sqrt(2 * self.len) * counter * (1 - counter)
            p_value = math.erf(num / denom)
        else:
            p_value = 0
        return p_value > 0.01

    def split_bits(self) -> list:
        blocks = []
        quantity = (self.len // 8) * 8
        for i in range(0, quantity, 8):
            block = self.sequence[i : i + 8]
            blocks.append(block)
        return blocks

    def largest_number_of_units(self, blocks: list) -> dict:
        unit_counts = {}
        for block in blocks:
            counter = 0
            max_counter = 0
            for i in block:
                if int(i) == 1:
                    counter += 1
                    max_counter = max(max_counter, counter)
                else:
                    counter = 0
            if max_counter in unit_counts:
                unit_counts[max_counter] += 1
            else:
                unit_counts[max_counter] = 1
        sorted_dict = dict(sorted(unit_counts.items(), key=lambda x: x[1]))
        return sorted_dict

    def length_test(self, dictionary: dict) -> bool:
        try:
            pi = dict()
            pi[1] = 0.2148
            pi[2] = 0.3672
            pi[3] = 0.2305
            pi[4] = 0.1875
            pi[5] = 0.1445
            square_x = 0
            for i, value in dictionary.items():
                square_x += pow(value - 16 * pi[i], 2) / (16 * pi[i])
            p_value = scipy.special.gammainc(3 / 2, square_x / 2)
            return p_value > 0.01
        except Exception as ex:
            logging.error(
                f"Length of the dictionary is greater than number of pi-constants: {ex.message}\n{ex.args}\n"
            )


if __name__ == "__main__":
    sequence = NistTest(
        "011111011010010100000110101100111010011011100011100100001110111011100101101101111110010011101001011000101010100010111101000111100"
    )
    print(sequence.bitwise_test())
    print(sequence.same_bits_test())
    print(sequence.split_bits())
    my_dict = sequence.largest_number_of_units(sequence.split_bits())
    print(sequence.length_test(my_dict))
