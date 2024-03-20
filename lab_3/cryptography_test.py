import os
import logging
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import serialization, asymmetric, hashes, padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key


logging.basicConfig(level=logging.INFO)


class Cryptograthy:

    def __init__(self, symmetric_key: str, private_key: str, public_key: str) -> None:
        self.symmetric_key = symmetric_key
        self.private_key = private_key
        self.public_key = public_key
        self.key_size = 0

    def key_generation(self, key_size):
        # Генерация ключа для симметричного алгоритма
        self.key_size = key_size
        symmetric_key = os.urandom(key_size)  # это байты

        # Генерация ключа для ассимметричного алгоритма
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public_key = private_key.public_key()

        # сериализация открытого ключа в файл
        with open(self.public_key, "wb") as public_out:
            public_out.write(
                public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo,
                )
            )
        # сериализация закрытого ключа в файл
        with open(self.private_key, "wb") as private_out:
            private_out.write(
                private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption(),
                )
            )
        # Шифрование симметричного ключа с помощью ассиметричного
        encrypted_symmetric_key = public_key.encrypt(
            symmetric_key,
            asymmetric.padding.OAEP(
                mgf=asymmetric.padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        # Сериализация зашифрованного ключа симметричного алгоритма в файл
        with open(self.symmetric_key, "wb") as key_file:
            key_file.write(encrypted_symmetric_key)

    def encryption(self, text_file_path, encryption_file_path) -> None:
        with open(self.symmetric_key, mode="rb") as key_file:
            sym_key = key_file.read()
        with open(self.private_key, "rb") as pem_in:
            pr_key = pem_in.read()
        private_key = load_pem_private_key(pr_key, password=None)
        symmetric_key = private_key.decrypt(
            sym_key,
            asymmetric.padding.OAEP(
                mgf=asymmetric.padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        with open(text_file_path, "rb") as f:
            data = f.read()
        padder = padding.PKCS7(self.key_size * 8).padder()
        padded_text = padder.update(data) + padder.finalize()
        iv = os.urandom(self.key_size)
        cipher = Cipher(algorithms.TripleDES(symmetric_key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(padded_text) + encryptor.finalize()
        encrypted_data = iv + encrypted_data
        with open(encryption_file_path, "wb") as f:
            f.write(encrypted_data)

    def decryption(self, encryption_file_path, decryption_file_path):
        with open(self.symmetric_key, mode="rb") as key_file:
            sym_key = key_file.read()
        with open(self.private_key, "rb") as pem_in:
            pr_key = pem_in.read()
        private_key = load_pem_private_key(pr_key, password=None)
        symmetric_key = private_key.decrypt(
            sym_key,
            asymmetric.padding.OAEP(
                mgf=asymmetric.padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        with open(encryption_file_path, "rb") as f:
            encrypted_data = f.read()
        iv = encrypted_data[: self.key_size]
        encrypted_data = encrypted_data[self.key_size :]
        cipher = Cipher(algorithms.TripleDES(symmetric_key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        data = decryptor.update(encrypted_data) + decryptor.finalize()
        unpadder = padding.PKCS7(self.key_size * 8).unpadder()
        data = unpadder.update(data) + unpadder.finalize()
        # Сохранение расшифрованных данных в файл
        try:
            with open(decryption_file_path, "wb") as f:
                f.write(data)
        except Exception as e:
            logging.error(e)


if __name__ == "__main__":

    my_key = Cryptograthy(
        "lab_3\symmetric.txt", "lab_3\private.pem", "lab_3\public.pem"
    )
    my_key.key_generation(8)
    my_key.encryption("lab_3/base_text.txt", "encryption_text.txt")
    my_key.decryption("encryption_text.txt", "decryption_text.txt")
