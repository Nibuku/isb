import os
import logging
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import serialization, asymmetric, hashes, padding


logging.basicConfig(level=logging.INFO)


class Cryptograthy:

    def __init__(self, symmetric_key: str, private_key: str, public_key: str) -> None:
        self.symmetric_key = symmetric_key
        self.private_key = private_key
        self.public_key = public_key

    def key_generation(self, key_size):
        # Генерация ключа для симметричного алгоритма
        symmetric_key= os.urandom(key_size)  # это байты

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
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
        )
        # Сериализация зашифрованного ключа симметричного алгоритма в файл
        with open(self.symmetric_key, 'wb') as key_file:
            key_file.write(encrypted_symmetric_key)






if __name__ == "__main__":

    
