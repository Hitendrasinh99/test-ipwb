import json

def xor_decrypt(data: bytes, key: bytes) -> bytes:
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

def parse_cdxj(file_path):
    entries = []
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith('!'):
                continue
            _, json_str = line.strip().split(" ", 1)
            entries.append(json.loads(json_str))
    return entries
