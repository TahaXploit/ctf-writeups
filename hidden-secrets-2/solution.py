# bruteforce_xor.py
from PIL import Image
import itertools
import string

def extract_bytes_from_lsb(img_path):
    img = Image.open(img_path)
    pixels = img.load()
    width, height = img.size

    bits = []
    for y in range(height):
        for x in range(width):
            r,g,b = pixels[x,y]
            bits.append(r & 1); bits.append(g & 1); bits.append(b & 1)

    out = bytearray()
    for i in range(0, len(bits), 8):
        byte = 0
        for j in range(8):
            if i + j < len(bits):
                byte = (byte << 1) | bits[i + j]
            else:
                byte = (byte << 1)
        out.append(byte)
    return bytes(out)

def xor_bytes(data, key):
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

def looks_like_ascii(b):
    try:
        s = b.decode('ascii')
    except:
        return False
    # simple check for flag format
    return s.startswith("CGLITCHERS{") and '}' in s

if __name__ == "__main__":
    raw = extract_bytes_from_lsb("CGLITCHERS1.png")
    payload_len = int.from_bytes(raw[0:2], "big")
    payload = raw[2:2+payload_len]
    print("payload length:", payload_len)

    # Strategy: try short keys from a small wordlist and printable bytes
    # first try a handful of obvious small words:
    wordlist = ["Nein", "test", "key", "pass", "love", "salt"]
    for w in wordlist:
        flag = xor_bytes(payload, w.encode())
        if looks_like_ascii(flag):
            print("FOUND with wordlist key:", w, flag)
            raise SystemExit(0)

    # fallback: brute-force 1-3 byte keys (printable)
    printable = list(range(32, 127))
    for L in (1,2,3):
        print("trying key length", L)
        for key_tuple in itertools.product(printable, repeat=L):
            key = bytes(key_tuple)
            flag = xor_bytes(payload, key)
            if looks_like_ascii(flag):
                print("found key:", key, "flag:", flag)
                raise SystemExit(0)
    print("no key found (increase key length or add wordlist).")
