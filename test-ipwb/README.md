test-ipwb
---
A demo project to simulate how [IPWB](https://github.com/oduwsdl/ipwb) (InterPlanetary Wayback) handles encryption in CDXJ metadata focusing on legacy `XOR` and current `AES` encryption support.

Why This Project?
---
The IPWB tool indexes and replays web archives. It originally supported `XOR` encryption for metadata in `.cdxj` files. Later, IPWB switched to more secure `AES` encryption using `pycryptodome`. However, **older CDXJ files using XOR break compatibility**, as IPWB assumes AES by default and shows gibberish output.

This project:
---
- Simulates both encryption methods
- Checks the declared encryption type in `.cdxj` metadata
- Handles legacy XOR manually
- Fails gracefully for unsupported methods
  
This directly relates to the IPWB GitHub issue [#448](https://github.com/oduwsdl/ipwb/issues/448).

Purpose
---
- Demonstrate encryption/decryption of CDXJ entries  
- Read and validate encryption method from CDXJ metadata  
- Avoid crashing when unsupported encryption types are used  
- Show how `AES` and `XOR` differ in handling  
- Help future-proof IPWB by simulating legacy compatibility

How It Works
---
The project contains:
> `data/`
Stores:
- `encrypted-xor.bin` — XOR-encrypted URL
- `encrypted-aes.bin` — AES-encrypted URL
- `metadata.cdxj` — metadata describing encryption method and URL

> `encrypt.py`
- Encrypts one URL with `XOR`, one with `AES`
- Saves binary data to `/data/`
- Writes metadata to `metadata.cdxj` file
- Prints the keys to use during decryption

> `decrypt.py`
- Loads `metadata.cdxj`
- For each record Detects encryption type
- If `AES`, asks for AES base64 key and decrypts
- If `XOR`, asks for XOR key string and decrypts
- If anything else → shows a clean error

> `utils.py`
- Reusable helper functions:
- `xor_decrypt()` — Manual XOR decryption logic
- `parse_cdxj()` — Reads CDXJ file and returns metadata records

How to Run the Project
---
Step 1: Clone or Download
Open a terminal or VS Code and navigate to your working folder:
```bash
git clone https://github.com/Hitendrasinh99/test-ipwb.git
cd test-ipwb
```
---
Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```
---
Step 3: Encrypt URLs
This will create AES/XOR encrypted binary files, generate a single metadata.cdxj metadata file, and print the required decryption keys.
```bash
python encrypt.py
```
---
Step 4: Decrypt URLs
This will read the metadata from metadata.cdxj, prompt for the correct key per method, and print the decrypted original URLs.
```bash
python decrypt.py
```

Why is this needed?
---
In real IPWB environments:
- Older `.cdxj` files might still declare `"encryption": "XOR"`
- IPWB now defaults to AES, which can't decrypt XOR properly
- If we don’t check the encryption method first, replay will fail
Main logic in `decrypt.py`
```python
if method == "AES":
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ct), AES.block_size)
elif method == "XOR":
    return xor_decrypt(data, key.encode())
else:
    raise ValueError("Unsupported encryption method")
```
