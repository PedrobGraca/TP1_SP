import os
import time
import numpy as np
from cryptography.hazmat.primitives import hashes

DATA_DIR = "../1_data"
RESULTS = []

def sha256(data):
    digest = hashes.Hash(hashes.SHA256())
    digest.update(data)
    return digest.finalize()

def benchmark(file_path, runs=30):
    with open(file_path, "rb") as f:
        data = f.read()

    times = []

    for _ in range(runs):
        start = time.perf_counter()
        _ = sha256(data)
        end = time.perf_counter()

        times.append((end - start) * 1e6)  # microseconds

    return {
        "file": os.path.basename(file_path),
        "size": len(data),
        "avg": np.mean(times),
        "std": np.std(times),
    }

def main():
    files = sorted(os.listdir(DATA_DIR), key=lambda x: int(x.split('_')[1][:-5]))

    print("\n SHA-256 Benchmark iniciado...\n")

    for file in files:
        print(f" A processar: {file}...")

        path = os.path.join(DATA_DIR, file)
        result = benchmark(path)
        RESULTS.append(result)

        print(f"[{file}]")
        print(f"  Hash: {result['avg']:.2f} µs (± {result['std']:.2f})\n")

    np.save("../3_results/3_sha_results.npy", RESULTS)

    print(" Benchmark SHA-256 concluído.")

if __name__ == "__main__":
    main()