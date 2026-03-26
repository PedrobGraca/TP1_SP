import os
import time
import numpy as np
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# Configuração
DATA_DIR = "../1_data"
RESULTS = []

# Chave AES-256 (32 bytes)
KEY = os.urandom(32)

def aes_encrypt(data):
    nonce = os.urandom(16)
    cipher = Cipher(algorithms.AES(KEY), modes.CTR(nonce))
    encryptor = cipher.encryptor()
    return nonce + encryptor.update(data) + encryptor.finalize()

def aes_decrypt(ciphertext):
    nonce = ciphertext[:16]
    cipher = Cipher(algorithms.AES(KEY), modes.CTR(nonce))
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext[16:]) + decryptor.finalize()

def benchmark(file_path, runs=30):
    with open(file_path, "rb") as f:
        data = f.read()

    enc_times = []
    dec_times = []

    for _ in range(runs):
        # Encrypt timing
        start = time.perf_counter()
        ciphertext = aes_encrypt(data)
        end = time.perf_counter()
        enc_times.append((end - start) * 1e6)  # microseconds

        # Decrypt timing
        start = time.perf_counter()
        _ = aes_decrypt(ciphertext)
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

    print("\n AES Benchmark iniciado...\n")

    for file in files:
        path = os.path.join(DATA_DIR, file)
        result = benchmark(path)
        RESULTS.append(result)

        print(f"[{file}]")
        print(f"  Encrypt: {result['enc_avg']:.2f} µs (± {result['enc_std']:.2f})")
        print(f"  Decrypt: {result['dec_avg']:.2f} µs (± {result['dec_std']:.2f})\n")

    # Guardar resultados
    np.save("../3_results/1_aes_results.npy", RESULTS)

    print("Benchmark AES concluído e guardado.")

if __name__ == "__main__":
    main()