import os # Módulo para interagir com o sistema operacional, como criar diretórios e arquivos

# Tamanhos em bytes
file_sizes = [8, 64, 512, 4096, 32768, 262144, 2097152]

output_dir = "../1_data" # Diretório onde os ficheiros serão salvos

os.makedirs(output_dir, exist_ok=True) # Cria o diretório se ele não existir
counter = 0 #contador para mostrar o número do ficheiro criado, não tem impacto na geração dos ficheiros

for size in file_sizes:
    filename = f"{output_dir}/file_{size}B.bin"
    counter += 1 

    # Dados aleatórios seguros
    data = os.urandom(size)
    
    with open(filename, "wb") as f: # Abre o arquivo para escrita em modo binário
        f.write(data) # Escreve os dados aleatórios no arquivo
    
    print(f"{counter}º Ficheiro criado: {filename} ({size} bytes)")

print("\n--- Todos os ficheiros foram gerados com sucesso. ---")