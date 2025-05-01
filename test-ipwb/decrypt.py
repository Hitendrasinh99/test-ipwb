from utils import xor_decrypt, parse_cdxj
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def decrypt_entry(path, method, key):
    with open(path, 'rb') as f:
        data = f.read()

    if method == "AES":
        iv, ct = data[:16], data[16:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(ct), AES.block_size).decode()
    elif method == "XOR":
        return xor_decrypt(data, key.encode()).decode()
    else:
        raise ValueError(f"[!] Unsupported encryption method: {method}")

if __name__ == "__main__":
    entries = parse_cdxj("data/metadata.cdxj")
    for i, record in enumerate(entries):
        print(f"\n== Decrypting Record #{i+1} [{record['encryption']}] ==")
        if record["encryption"] == "AES":
            aes_key = base64.b64decode(input("Enter AES key (base64): "))
            url = decrypt_entry("data/encrypted-aes.bin", "AES", aes_key)
        elif record["encryption"] == "XOR":
            xor_key = input("Enter XOR key (string): ")
            url = decrypt_entry("data/encrypted-xor.bin", "XOR", xor_key)
        else:
            print("Unsupported encryption method, skipping.")
            continue
        print("Decrypted URL:", url)
