import os
import time
import numpy as np
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

DATA_DIR = "../1_data"
RESULTS = []

# Gerar chave RSA (uma vez)
PRIVATE_KEY = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
PUBLIC_KEY = PRIVATE_KEY.public_key()

BLOCK_SIZE = 32  # SHA256 output = 32 bytes

def sha256(data):
    digest = hashes.Hash(hashes.SHA256())
    digest.update(data)
    return digest.finalize()

def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

# Encrypt
def rsa_encrypt(data):
    r = os.urandom(32)

    # RSA(r)
    enc_r = PUBLIC_KEY.encrypt(
        r,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    ciphertext_blocks = []

    for i in range(0, len(data), BLOCK_SIZE):
        block = data[i:i+BLOCK_SIZE]

        # H(i, r)
        h = sha256(i.to_bytes(4, 'big') + r)

        cipher_block = xor_bytes(block, h[:len(block)])
        ciphertext_blocks.append(cipher_block)

    return enc_r, b''.join(ciphertext_blocks)

# Decrypt
def rsa_decrypt(enc_r, ciphertext):
    # recuperar r
    r = PRIVATE_KEY.decrypt(
        enc_r,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    plaintext_blocks = []

    for i in range(0, len(ciphertext), BLOCK_SIZE):
        block = ciphertext[i:i+BLOCK_SIZE]

        h = sha256(i.to_bytes(4, 'big') + r)

        plain_block = xor_bytes(block, h[:len(block)])
        plaintext_blocks.append(plain_block)

    return b''.join(plaintext_blocks)

def benchmark(file_path, runs=3): #runs=10 para reduzir o tempo de execução, já que RSA é mais lento que AES
    with open(file_path, "rb") as f:
        data = f.read()

    enc_times = []
    dec_times = []

    for _ in range(runs):
        # Encrypt
        start = time.perf_counter()
        enc_r, ciphertext = rsa_encrypt(data)
        end = time.perf_counter()
        enc_times.append((end - start) * 1e6)

        # Decrypt
        start = time.perf_counter()
        _ = rsa_decrypt(enc_r, ciphertext)
        end = time.perf_counter()
        dec_times.append((end - start) * 1e6)

    return {
        "file": os.path.basename(file_path),
        "size": len(data),
        "enc_avg": np.mean(enc_times),
        "enc_std": np.std(enc_times),
        "dec_avg": np.mean(dec_times),
        "dec_std": np.std(dec_times),
    }

def main():
    files = sorted(os.listdir(DATA_DIR), key=lambda x: int(x.split('_')[1][:-5]))
    #files = ["file_8B.bin","file_64B.bin","file_512B.bin", "file_4096B.bin"] # PARA TESTAR TODOS OS FICHEIROS, escepto o que PODE DEMORAR MUITO TEMPO

    print("\n RSA Benchmark iniciado...\n")

    for file in files:
        print(f" A processar: {file}...")  # ADICIONADO PARA INDICAR QUAL FICHEIRO ESTÁ SENDO PROCESSADO, ÚTIL PARA FICHEIROS MAIORES QUE PODEM DEMORAR MUITO TEMPO

        path = os.path.join(DATA_DIR, file)
        result = benchmark(path)
        RESULTS.append(result)

        print(f"[{file}]")
        print(f"  Encrypt: {result['enc_avg']:.2f} µs (± {result['enc_std']:.2f})")
        print(f"  Decrypt: {result['dec_avg']:.2f} µs (± {result['dec_std']:.2f})\n")

    np.save("../3_results/2_rsa_results.npy", RESULTS)
    print(" Benchmark RSA concluído.")

if __name__ == "__main__":
    main()