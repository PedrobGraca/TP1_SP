from aes_module import generate_aes_key, generate_nonce, aes_encrypt, aes_decrypt
from rsa_module import generate_rsa_keys, rsa_based_encrypt, rsa_based_decrypt
from sha_module import sha256_hexdigest

data = b"Ola mundo"

# AES
key = generate_aes_key()
nonce = generate_nonce()
ciphertext = aes_encrypt(data, key, nonce)
plaintext = aes_decrypt(ciphertext, key, nonce)

print("AES correto?", plaintext == data)

# RSA-based
private_key, public_key = generate_rsa_keys()
encrypted_r, cipher_blocks = rsa_based_encrypt(data, public_key)
recovered = rsa_based_decrypt(encrypted_r, cipher_blocks, private_key)

print("RSA correto?", recovered == data)

# SHA-256
print("SHA-256:", sha256_hexdigest(data))