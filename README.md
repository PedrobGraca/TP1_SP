# Segurança e Privacidade – Trabalho Prático 1

## Descrição do Projeto
Este projeto foi desenvolvido no âmbito da unidade curricular **Segurança e Privacidade** e tem como objetivo avaliar o desempenho de diferentes mecanismos criptográficos em Python.

O trabalho consiste na medição e análise de tempos de execução de:
- AES-256 (criptografia simétrica)
- RSA (criptografia assimétrica com esquema híbrido)
- SHA-256 (função de hash)

Os testes foram realizados sobre ficheiros de diferentes tamanhos, permitindo comparar eficiência, escalabilidade e comportamento dos algoritmos.



## Objetivos
- Implementar algoritmos criptográficos em Python
- Medir tempos de execução
- Comparar desempenho entre algoritmos:
    - AES vs RSA
    - AES vs SHA-256
    - Encrypt vs Decrypt (RSA)
- Produzir gráficos e análise dos resultados



## Tecnologias Utilizadas
- Python 3.12
- Bibliotecas:
    - cryptography
    - numpy
    - matplotlib



## Estrutura do Projeto
```
/project
├── /1_data                  # Ficheiros para testes(gerados pelo script 0)
├── /2_scripts               # Scripts principais do projeto
│   ├── 0_generate_files.py
│   ├── 1_aes_test.py
│   ├── 2_rsa_test.py
│   └── 3_sha_test.py
├── /3_results               # Resultados em formato .npy de cada criptografia
├── /4_plots                 # Gráficos de comparação(gerados pelo script 4)
├── /5_report                # Relatório do projeto
└── README.md                # Este ficheiro
```
---

## Como Executar

### Pré-requisitos
- Python 3.10 ou superior (recomendado 3.12)
- pip instalado

### Instalar dependências
```
pip install cryptography numpy matplotlib
```

### Executar

#### **1. Gerar ficheiros de teste:**
```
python scripts/0_generate_files.py
```
#### **2. AES:**
```
python scripts/1_aes_test.py
```

#### **3. RSA:**
```
python scripts/2_rsa_test.py
```

#### **4. SHA:**
```
python scripts/3_sha_test.py
```



## Resultados
- **AES:** 
    - Crescimento linear
    - Muito eficiente para grandes volumes
    - Encrypt ≈ Decrypt
- **RSA:**
    - Muito mais lento (~100x que AES)
    - Não escalável para grandes ficheiros
    - Decrypt geralmente mais lento que Encrypt
- **SHA-256:** 
    - Crescimento linear
    - Mais rápido
    - Não fornece confidencialidade, apenas integridade (sem criptografia)

---

### Notas Importantes
- O tempo de I/O (leitura/escrita de ficheiros) não foi considerado nas medições
- Cada teste foi executado múltiplas vezes para garantir consistência estatística
- Dados aleatórios foram utilizados para evitar viés nos resultados

## Participantes do Projeto
- [Ezequiel Tchimbaya Cachapeu Paulo](https://github.com/ezequielcabeja) (up202400891)
- [Pedro Emanuel Brazão da Graça](https://github.com/PedrobGraca) (up202406955)
- [Victor de Vargas Lopes](https://github.com/vituvvl) (up202400863)
