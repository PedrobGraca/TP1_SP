import os
import struct
import hashlib
from typing import Tuple, List

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes


BLOCK_SIZE = 32  # 32 bytes, porque SHA-256 produz 32 bytes


def generate_rsa_keys(key_size: int = 2048):
    """
    Gera par de chaves RSA.
    Retorna (private_key, public_key).
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size
    )
    public_key = private_key.public_key()
    return private_key, public_key


def xor_bytes(a: bytes, b: bytes) -> bytes:
    """
    Faz XOR entre dois arrays de bytes com o mesmo tamanho.
    """
    return bytes(x ^ y for x, y in zip(a, b))


def int_to_4bytes(i: int) -> bytes:
    """
    Converte inteiro em 4 bytes (big endian).
    """
    return struct.pack(">I", i)


def generate_mask(block_index: int, r: bytes, output_size: int) -> bytes:
    """
    Gera máscara pseudoaleatória baseada em SHA-256 a partir de (block_index, r).

    Como SHA-256 devolve 32 bytes, se o bloco for maior do que 32,
    concatenamos vários hashes até atingir output_size.
    """
    mask = b""
    counter = 0

    while len(mask) < output_size:
        data = int_to_4bytes(block_index) + int_to_4bytes(counter) + r
        mask += hashlib.sha256(data).digest()
        counter += 1

    return mask[:output_size]


def split_into_blocks(data: bytes, block_size: int = BLOCK_SIZE) -> List[bytes]:
    """
    Divide os dados em blocos.
    """
    return [data[i:i + block_size] for i in range(0, len(data), block_size)]


def rsa_based_encrypt(data: bytes, public_key) -> Tuple[bytes, List[bytes]]:
    """
    Encriptação híbrida baseada no esquema do enunciado.

    Passos:
    1. Gera um valor aleatório r
    2. Encripta r com RSA
    3. Divide a mensagem em blocos
    4. Para cada bloco m_i, calcula H(i, r) e faz XOR com m_i

    Retorna:
    - encrypted_r: r encriptado com RSA
    - cipher_blocks: lista de blocos cifrados
    """
    # r com 32 bytes
    r = os.urandom(32)

    encrypted_r = public_key.encrypt(
        r,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    plaintext_blocks = split_into_blocks(data, BLOCK_SIZE)
    cipher_blocks = []

    for i, block in enumerate(plaintext_blocks):
        mask = generate_mask(i, r, len(block))
        cipher_block = xor_bytes(block, mask)
        cipher_blocks.append(cipher_block)

    return encrypted_r, cipher_blocks


def rsa_based_decrypt(encrypted_r: bytes, cipher_blocks: List[bytes], private_key) -> bytes:
    """
    Desencriptação do esquema híbrido.

    Passos:
    1. Recupera r com RSA
    2. Para cada bloco cifrado c_i, calcula H(i, r)
    3. Faz XOR para obter o bloco original
    4. Junta todos os blocos
    """
    r = private_key.decrypt(
        encrypted_r,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    plaintext_blocks = []

    for i, cipher_block in enumerate(cipher_blocks):
        mask = generate_mask(i, r, len(cipher_block))
        plaintext_block = xor_bytes(cipher_block, mask)
        plaintext_blocks.append(plaintext_block)

    return b"".join(plaintext_blocks)


if __name__ == "__main__":
    # Pequeno teste
    private_key, public_key = generate_rsa_keys()

    original = b"Este e um teste do esquema RSA-based com SHA-256." * 5

    encrypted_r, cipher_blocks = rsa_based_encrypt(original, public_key)
    recovered = rsa_based_decrypt(encrypted_r, cipher_blocks, private_key)

    print("Original recuperado corretamente?", original == recovered)
    print("Numero de blocos:", len(cipher_blocks))


    fjofwo