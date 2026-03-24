import os


FILE_SIZES = [
    8,
    64,
    512,
    4096,
    32768,
    262144,
    2097152
]


def ensure_data_folder(folder_path: str = "data") -> None:
    """
    Garante que a pasta de destino existe.
    """
    os.makedirs(folder_path, exist_ok=True)


def generate_random_file(size: int, folder_path: str = "data") -> str:
    """
    Gera um ficheiro binário aleatório com o tamanho indicado.

    Retorna o caminho do ficheiro criado.
    """
    ensure_data_folder(folder_path)

    file_path = os.path.join(folder_path, f"file_{size}.bin")

    with open(file_path, "wb") as file:
        file.write(os.urandom(size))

    return file_path


def generate_all_files(folder_path: str = "data") -> None:
    """
    Gera todos os ficheiros pedidos no enunciado.
    """
    print("A gerar ficheiros aleatórios...\n")

    for size in FILE_SIZES:
        file_path = generate_random_file(size, folder_path)
        print(f"Criado: {file_path} ({size} bytes)")

    print("\nTodos os ficheiros foram gerados com sucesso.")


if __name__ == "__main__":
    generate_all_files()