import os
import logging
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import serialization, asymmetric, hashes, padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key


logging.basicConfig(level=logging.INFO)


class Cryptograthy:
    """Class of hybrid cryptosystem. Symmetric Triple Des encryption algorithm, Asymmetric RSA.
    Methods:
        1.key_generation(self)->None
        2.encryption(self, text_file_path:str, encryption_file_path:str) -> None
        3.decryption(self, encryption_file_path:str, decryption_file_path:str)->None:
    """

    def __init__(
        self, symmetric_key: str, private_key: str, public_key: str, key_size: int
    ) -> None:
        """parameters:
        symmetric_key: the path by which to serialize the encrypted symmetric key;
        public_key: the path by which to serialize the public key;
        private_key: the path to serialize the private key;
        key_size: the key size is at the user's choice (8, 16 or 24 bytes)"""
        self.symmetric_key = symmetric_key
        self.private_key = private_key
        self.public_key = public_key
        self.key_size = key_size

    def key_generation(self) -> None:
        """The function which:
        1.1. Generate a key for the symmetric algorithm.
        1.2. Generate keys for the asymmetric algorithm.
        1.3. Serialize asymmetric keys.
        1.4. Encrypt the symmetric encryption key with a public key and save it in the specified path.
        """
        symmetric_key = os.urandom(self.key_size)
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public_key = private_key.public_key()
        try:
            with open(self.public_key, "wb") as public_out:
                public_out.write(
                    public_key.public_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PublicFormat.SubjectPublicKeyInfo,
                    )
                )
        except Exception as ex:
            logging.error(
                f"Error serializing the public key to a file: {ex.message}\n{ex.args}\n"
            )
        try:
            with open(self.private_key, "wb") as private_out:
                private_out.write(
                    private_key.private_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PrivateFormat.TraditionalOpenSSL,
                        encryption_algorithm=serialization.NoEncryption(),
                    )
                )
        except Exception as ex:
            logging.error(
                f"Error serializing the private key to a file: {ex.message}\n{ex.args}\n"
            )
        encrypted_symmetric_key = public_key.encrypt(
            symmetric_key,
            asymmetric.padding.OAEP(
                mgf=asymmetric.padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        try:
            with open(self.symmetric_key, "wb") as key_file:
                key_file.write(encrypted_symmetric_key)
        except Exception as ex:
            logging.error(
                f"Error serializing the symmetric key to a file: {ex.message}\n{ex.args}\n"
            )

    def encryption(self, text_file_path: str, encryption_file_path: str) -> None:
        """parameters:
        text_file_path:the path to the encrypted text file;
        encryption_file_path: the path to save the encrypted text file;
        the function which:
            2.1. Decrypt the symmetric key.
            2.2. Encrypt the text using a symmetric algorithm and save it along the specified path.
        """
        try:
            with open(self.symmetric_key, mode="rb") as key_file:
                sym_key = key_file.read()
        except Exception as ex:
            logging.error(
                f"Error deserelizations the symmetric key: {ex.message}\n{ex.args}\n"
            )
        try:
            with open(self.private_key, "rb") as pem_in:
                pr_key = pem_in.read()
        except Exception as ex:
            logging.error(
                f"Error deserelizations the private key: {ex.message}\n{ex.args}\n"
            )
        private_key = load_pem_private_key(pr_key, password=None)
        symmetric_key = private_key.decrypt(
            sym_key,
            asymmetric.padding.OAEP(
                mgf=asymmetric.padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        try:
            with open(text_file_path, "rb") as f:
                data = f.read()
        except Exception as ex:
            logging.error(f"File reading error: {ex.message}\n{ex.args}\n")
        padder = padding.PKCS7(self.key_size * 8).padder()
        padded_text = padder.update(data) + padder.finalize()
        iv = os.urandom(self.key_size)
        cipher = Cipher(algorithms.TripleDES(symmetric_key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(padded_text) + encryptor.finalize()
        encrypted_data = iv + encrypted_data
        try:
            with open(encryption_file_path, "wb") as f:
                f.write(encrypted_data)
        except Exception as ex:
            logging.error(f"File writing error: {ex.message}\n{ex.args}\n")

    def decryption(self, encryption_file_path: str, decryption_file_path: str) -> None:
        """parameters:
            encryption_file_path: the path to the encrypted text file;
            decryption_file_path: the path to save the decrypted text file.
        the function which:
            3.1. Decrypt the symmetric key.
            3.2. Decrypt the text using a symmetric algorithm and save it along the specified path.
        """
        try:
            with open(self.symmetric_key, mode="rb") as key_file:
                sym_key = key_file.read()
        except Exception as ex:
            logging.error(
                f"Error deserelizations the symmetric key: {ex.message}\n{ex.args}\n"
            )
        try:
            with open(self.private_key, "rb") as pem_in:
                pr_key = pem_in.read()
        except Exception as ex:
            logging.error(
                f"Error deserelizations the private key: {ex.message}\n{ex.args}\n"
            )
        private_key = load_pem_private_key(pr_key, password=None)
        symmetric_key = private_key.decrypt(
            sym_key,
            asymmetric.padding.OAEP(
                mgf=asymmetric.padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        try:
            with open(encryption_file_path, "rb") as f:
                encrypted_data = f.read()
        except Exception as ex:
            logging.error(f"File reading error: {ex.message}\n{ex.args}\n")
        iv = encrypted_data[: self.key_size]
        encrypted_data = encrypted_data[self.key_size :]
        cipher = Cipher(algorithms.TripleDES(symmetric_key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        data = decryptor.update(encrypted_data) + decryptor.finalize()
        unpadder = padding.PKCS7(self.key_size * 8).unpadder()
        data = unpadder.update(data) + unpadder.finalize()
        try:
            with open(decryption_file_path, "wb") as f:
                f.write(data)
        except Exception as e:
            logging.error(f"File writing error: {ex.message}\n{ex.args}\n")
