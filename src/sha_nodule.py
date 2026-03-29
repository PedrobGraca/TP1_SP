import hashlib


def sha256_digest(data: bytes) -> bytes:
    """
    Calcula o digest SHA-256 dos dados.
    Retorna os 32 bytes do hash.
    """
    return hashlib.sha256(data).digest()


def sha256_hexdigest(data: bytes) -> str:
    """
    Calcula o SHA-256 e devolve em formato hexadecimal.
    """
    return hashlib.sha256(data).hexdigest()


if __name__ == "__main__":
    # Pequeno teste
    data = b"Teste SHA-256"

    digest_bytes = sha256_digest(data)
    digest_hex = sha256_hexdigest(data)

    print("Dados       :", data)
    print("Digest bytes:", digest_bytes)
    print("Digest hex  :", digest_hex)