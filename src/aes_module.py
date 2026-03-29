from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os


def generate_aes_key() -> bytes:
    """
    Gera uma chave AES-256 (32 bytes = 256 bits).
    """
    return os.urandom(32)


def generate_nonce() -> bytes:
    """
    Gera um nonce de 16 bytes para AES-CTR.
    """
    return os.urandom(16)


def aes_encrypt(data: bytes, key: bytes, nonce: bytes) -> bytes:
    """
    Encripta dados usando AES-CTR.
    """
    cipher = Cipher(algorithms.AES(key), modes.CTR(nonce))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(data) + encryptor.finalize()
    return ciphertext


def aes_decrypt(ciphertext: bytes, key: bytes, nonce: bytes) -> bytes:
    """
    Desencripta dados usando AES-CTR.
    """
    cipher = Cipher(algorithms.AES(key), modes.CTR(nonce))
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext


if __name__ == "__main__":
    # Pequeno teste
    original = b"Teste AES CTR"
    key = generate_aes_key()
    nonce = generate_nonce()

    encrypted = aes_encrypt(original, key, nonce)
    decrypted = aes_decrypt(encrypted, key, nonce)

    print("Original :", original)
    print("Encrypted:", encrypted)
    print("Decrypted:", decrypted)
    print("Correto? :", original == decrypted)