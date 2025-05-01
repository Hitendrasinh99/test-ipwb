from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
import base64
import os
import json

def xor_encrypt(data: bytes, key: bytes) -> bytes:
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

def aes_encrypt(data: bytes, key: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_CBC)
    ct = cipher.encrypt(pad(data, AES.block_size))
    return cipher.iv + ct

def write_combined_metadata(filepath, xor_url, aes_url):
    with open(filepath, "w") as f:
        f.write('!meta {"format": "cdxj", "version": "1.0"}\n')
        f.write('20190521202300 {"url": "' + xor_url + '", "mime": "text/html", "status": "200", "encryption": "XOR"}\n')
        f.write('20190521202400 {"url": "' + aes_url + '", "mime": "text/html", "status": "200", "encryption": "AES"}\n')

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)

    # Define URLs
    xor_url = "https://bafybeiarvv52gujxeausrn25pkhtah4jr4hkwh4zf2rydy5wy7tgej4gca.ipfs.dweb.link?filename=1.png"
    aes_url = "https://bafybeihgi7pav4naqk7nmuevjvylcrkl2dmnqi2ai7fgqxlqzignyebgfm.ipfs.dweb.link?filename=Shiv-Bhagwan.jpg"

    # Encrypt XOR
    xor_key = b"myxor"
    xor_encrypted = xor_encrypt(xor_url.encode(), xor_key)
    with open("data/encrypted-xor.bin", "wb") as f:
        f.write(xor_encrypted)

    # Encrypt AES
    aes_key = get_random_bytes(16)
    aes_encrypted = aes_encrypt(aes_url.encode(), aes_key)
    with open("data/encrypted-aes.bin", "wb") as f:
        f.write(aes_encrypted)

    # Write single metadata file
    write_combined_metadata("data/metadata.cdxj", xor_url, aes_url)

    print(f"[XOR KEY]  --> {xor_key.decode()}")
    print(f"[AES KEY]  --> {base64.b64encode(aes_key).decode()}")
