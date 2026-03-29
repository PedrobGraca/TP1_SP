import os
import csv
import platform
from datetime import datetime

from aes_module import generate_aes_key, generate_nonce, aes_encrypt, aes_decrypt
from rsa_module import generate_rsa_keys, rsa_based_encrypt, rsa_based_decrypt
from sha_module import sha256_digest
from benchmark_utils import benchmark_operation, compute_stats


DATA_FOLDER = "data"
RESULTS_FOLDER = "results"
RAW_RESULTS_FILE = os.path.join(RESULTS_FOLDER, "raw_results.csv")
SUMMARY_RESULTS_FILE = os.path.join(RESULTS_FOLDER, "summary_results.csv")
SYSTEM_INFO_FILE = os.path.join(RESULTS_FOLDER, "system_info.txt")

REPEATS = 30
WARMUP = 3


def ensure_results_folder() -> None:
    os.makedirs(RESULTS_FOLDER, exist_ok=True)


def list_data_files(folder_path: str = DATA_FOLDER) -> list[str]:
    """
    Lista os ficheiros .bin da pasta data, ordenados por tamanho extraído do nome.
    Ex.: file_8.bin, file_64.bin, ...
    """
    if not os.path.exists(folder_path):
        raise FileNotFoundError(
            f"A pasta '{folder_path}' não existe. Corre primeiro o generate_files.py."
        )

    files = [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if f.endswith(".bin")
    ]

    def extract_size(path: str) -> int:
        name = os.path.basename(path)
        # file_4096.bin -> 4096
        return int(name.replace("file_", "").replace(".bin", ""))

    files.sort(key=extract_size)
    return files


def read_file_bytes(file_path: str) -> bytes:
    with open(file_path, "rb") as file:
        return file.read()


def save_raw_results(rows: list[dict]) -> None:
    ensure_results_folder()

    fieldnames = [
        "algorithm",
        "operation",
        "file_name",
        "file_size",
        "run_number",
        "time_us",
    ]

    with open(RAW_RESULTS_FILE, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def save_summary_results(rows: list[dict]) -> None:
    ensure_results_folder()

    fieldnames = [
        "algorithm",
        "operation",
        "file_name",
        "file_size",
        "runs",
        "mean_us",
        "stdev_us",
        "min_us",
        "max_us",
        "median_us",
    ]

    with open(SUMMARY_RESULTS_FILE, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def save_system_info() -> None:
    ensure_results_folder()

    info_lines = [
        f"Timestamp: {datetime.now().isoformat()}",
        f"Platform: {platform.system()} {platform.release()}",
        f"Platform version: {platform.version()}",
        f"Machine: {platform.machine()}",
        f"Processor: {platform.processor()}",
        f"Python version: {platform.python_version()}",
        f"Repeats: {REPEATS}",
        f"Warmup: {WARMUP}",
    ]

    with open(SYSTEM_INFO_FILE, "w", encoding="utf-8") as file:
        file.write("\n".join(info_lines))


def build_raw_rows(
    algorithm: str,
    operation: str,
    file_name: str,
    file_size: int,
    times_us: list[float]
) -> list[dict]:
    rows = []

    for i, time_us in enumerate(times_us, start=1):
        rows.append({
            "algorithm": algorithm,
            "operation": operation,
            "file_name": file_name,
            "file_size": file_size,
            "run_number": i,
            "time_us": f"{time_us:.6f}",
        })

    return rows


def build_summary_row(
    algorithm: str,
    operation: str,
    file_name: str,
    file_size: int,
    stats: dict
) -> dict:
    return {
        "algorithm": algorithm,
        "operation": operation,
        "file_name": file_name,
        "file_size": file_size,
        "runs": stats["runs"],
        "mean_us": f"{stats['mean_us']:.6f}",
        "stdev_us": f"{stats['stdev_us']:.6f}",
        "min_us": f"{stats['min_us']:.6f}",
        "max_us": f"{stats['max_us']:.6f}",
        "median_us": f"{stats['median_us']:.6f}",
    }


def run_aes_benchmarks(file_path: str) -> tuple[list[dict], list[dict]]:
    file_name = os.path.basename(file_path)
    data = read_file_bytes(file_path)
    file_size = len(data)

    print(f"\n[AES] A processar {file_name} ({file_size} bytes)")

    key = generate_aes_key()
    nonce = generate_nonce()

    encrypt_times = benchmark_operation(
        aes_encrypt,
        data,
        key,
        nonce,
        repeats=REPEATS,
        warmup=WARMUP
    )

    ciphertext = aes_encrypt(data, key, nonce)

    decrypt_times = benchmark_operation(
        aes_decrypt,
        ciphertext,
        key,
        nonce,
        repeats=REPEATS,
        warmup=WARMUP
    )

    recovered = aes_decrypt(ciphertext, key, nonce)
    if recovered != data:
        raise ValueError(f"Erro AES: desencriptação falhou para {file_name}")

    encrypt_stats = compute_stats(encrypt_times)
    decrypt_stats = compute_stats(decrypt_times)

    raw_rows = []
    raw_rows.extend(build_raw_rows("AES", "encrypt", file_name, file_size, encrypt_times))
    raw_rows.extend(build_raw_rows("AES", "decrypt", file_name, file_size, decrypt_times))

    summary_rows = [
        build_summary_row("AES", "encrypt", file_name, file_size, encrypt_stats),
        build_summary_row("AES", "decrypt", file_name, file_size, decrypt_stats),
    ]

    return raw_rows, summary_rows


def run_rsa_benchmarks(file_path: str, private_key, public_key) -> tuple[list[dict], list[dict]]:
    file_name = os.path.basename(file_path)
    data = read_file_bytes(file_path)
    file_size = len(data)

    print(f"\n[RSA] A processar {file_name} ({file_size} bytes)")

    encrypt_times = benchmark_operation(
        rsa_based_encrypt,
        data,
        public_key,
        repeats=REPEATS,
        warmup=WARMUP
    )

    encrypted_r, cipher_blocks = rsa_based_encrypt(data, public_key)

    decrypt_times = benchmark_operation(
        rsa_based_decrypt,
        encrypted_r,
        cipher_blocks,
        private_key,
        repeats=REPEATS,
        warmup=WARMUP
    )

    recovered = rsa_based_decrypt(encrypted_r, cipher_blocks, private_key)
    if recovered != data:
        raise ValueError(f"Erro RSA-based: desencriptação falhou para {file_name}")

    encrypt_stats = compute_stats(encrypt_times)
    decrypt_stats = compute_stats(decrypt_times)

    raw_rows = []
    raw_rows.extend(build_raw_rows("RSA", "encrypt", file_name, file_size, encrypt_times))
    raw_rows.extend(build_raw_rows("RSA", "decrypt", file_name, file_size, decrypt_times))

    summary_rows = [
        build_summary_row("RSA", "encrypt", file_name, file_size, encrypt_stats),
        build_summary_row("RSA", "decrypt", file_name, file_size, decrypt_stats),
    ]

    return raw_rows, summary_rows


def run_sha_benchmarks(file_path: str) -> tuple[list[dict], list[dict]]:
    file_name = os.path.basename(file_path)
    data = read_file_bytes(file_path)
    file_size = len(data)

    print(f"\n[SHA-256] A processar {file_name} ({file_size} bytes)")

    digest_times = benchmark_operation(
        sha256_digest,
        data,
        repeats=REPEATS,
        warmup=WARMUP
    )

    _ = sha256_digest(data)

    digest_stats = compute_stats(digest_times)

    raw_rows = build_raw_rows("SHA256", "digest", file_name, file_size, digest_times)

    summary_rows = [
        build_summary_row("SHA256", "digest", file_name, file_size, digest_stats),
    ]

    return raw_rows, summary_rows


def main() -> None:
    ensure_results_folder()
    save_system_info()

    data_files = list_data_files()

    all_raw_rows = []
    all_summary_rows = []

    private_key, public_key = generate_rsa_keys()

    for file_path in data_files:
        aes_raw, aes_summary = run_aes_benchmarks(file_path)
        all_raw_rows.extend(aes_raw)
        all_summary_rows.extend(aes_summary)

        rsa_raw, rsa_summary = run_rsa_benchmarks(file_path, private_key, public_key)
        all_raw_rows.extend(rsa_raw)
        all_summary_rows.extend(rsa_summary)

        sha_raw, sha_summary = run_sha_benchmarks(file_path)
        all_raw_rows.extend(sha_raw)
        all_summary_rows.extend(sha_summary)

    save_raw_results(all_raw_rows)
    save_summary_results(all_summary_rows)

    print("\nBenchmark concluído com sucesso.")
    print(f"Raw results     -> {RAW_RESULTS_FILE}")
    print(f"Summary results -> {SUMMARY_RESULTS_FILE}")
    print(f"System info     -> {SYSTEM_INFO_FILE}")


if __name__ == "__main__":
    main()