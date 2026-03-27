import numpy as np
import matplotlib.pyplot as plt

# Carregar resultados
aes = np.load("../3_results/1_aes_results.npy", allow_pickle=True)
rsa = np.load("../3_results/2_rsa_results.npy", allow_pickle=True)
sha = np.load("../3_results/3_sha_results.npy", allow_pickle=True)

# Extrair dados
sizes = [r['size'] for r in aes]

aes_enc = [r['enc_avg'] for r in aes]
aes_dec = [r['dec_avg'] for r in aes]

rsa_enc = [r['enc_avg'] for r in rsa]
rsa_dec = [r['dec_avg'] for r in rsa]

sha_time = [r['avg'] for r in sha]

print(" Gráficos sendo gerados ...\n")

# Gráfico 1: AES vs RSA (Encrypt)
plt.figure()
plt.plot(sizes, aes_enc, marker='o', label='AES Encrypt')
plt.plot(sizes, rsa_enc, marker='o', label='RSA Encrypt')
plt.xlabel("File Size (bytes)")
plt.ylabel("Time (µs)")
plt.title("AES vs RSA Encryption Time")
plt.legend()
plt.grid()
plt.savefig("../4_plots/1_aes_vs_rsa_encrypt.png")

# Gráfico 2: AES vs SHA
plt.figure()
plt.plot(sizes, aes_enc, marker='o', label='AES Encrypt')
plt.plot(sizes, sha_time, marker='o', label='SHA-256')
plt.xlabel("File Size (bytes)")
plt.ylabel("Time (µs)")
plt.title("AES vs SHA-256")
plt.legend()
plt.grid()
plt.savefig("../4_plots/2_aes_vs_sha.png")

# Gráfico 3: RSA Encrypt vs Decrypt
plt.figure()
plt.plot(sizes, rsa_enc, marker='o', label='RSA Encrypt')
plt.plot(sizes, rsa_dec, marker='o', label='RSA Decrypt')
plt.xlabel("File Size (bytes)")
plt.ylabel("Time (µs)")
plt.title("RSA Encrypt vs Decrypt")
plt.legend()
plt.grid()
plt.savefig("../4_plots/3_rsa_enc_vs_dec.png")

# Gráfico 4: Todos juntos
plt.figure()
plt.plot(sizes, aes_enc, marker='o', label='AES')
plt.plot(sizes, rsa_enc, marker='o', label='RSA')
plt.plot(sizes, sha_time, marker='o', label='SHA-256')
plt.xlabel("File Size (bytes)")
plt.ylabel("Time (µs)")
plt.title("All Algorithms Comparison")
plt.legend()
plt.grid()
plt.savefig("../4_plots/4_all_comparison.png")

print(" Gráficos gerados com sucesso.")