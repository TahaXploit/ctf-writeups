# CGLITCHERS LSB XOR Steganography Writeup

**Category:** Steganography — LSB  
**File:** `CGLITCHERS1.png`  
**Flag format:** `CGLITCHERS{...}`  

---

## Challenge Description

The challenge provides a PNG image containing a hidden message. The hints indicate:

- The message is hidden in the **least significant bits (LSB)** of the pixels.
- The payload is encrypted using a **repeating XOR key**, possibly 4 bytes.
- The flag format is `CGLITCHERS{...}`.

Our goal is to extract the payload from the LSBs, decrypt it, and reveal the flag.

---

## Step 1: Inspect the image

Quick checks:
Command :
```bash
file CGLITCHERS1.png
```
Output : 
```bash
CGLITCHERS1.png: PNG image data, 800 x 2, 8-bit/color RGB, non-interlaced
```
Command :
```bash
zsteg -a CGLITCHERS1.png   # optional, shows LSB patterns
```
Output : 
```bash
[?] 47 bytes of extra data after image end (IEND), offset = 0xa9
extradata:0         .. text: "\n# decoy: nothing to see here xd , try harder.\n"
b1,r,lsb,xy         .. text: "\t'b+njoakXK"
b2,rgb,msb,xy       .. file: VISX image file
b2,bgr,msb,xy       .. file: VISX image file
b4,bgr,lsb,xy       .. file: AIX core file 64-bit
b5p,rgb,lsb,xy      .. file: PC formatted floppy with no filesystem
b6p,rgb,lsb,xy      .. file: MIT scheme (library?)
b8,r,msb,xy         .. file: RDI Acoustic Doppler Current Profiler (ADCP)
b8,g,msb,xy         .. file: RDI Acoustic Doppler Current Profiler (ADCP)
b8,b,msb,xy         .. file: RDI Acoustic Doppler Current Profiler (ADCP)
b8,rgb,msb,xy       .. file: RDI Acoustic Doppler Current Profiler (ADCP)
b8,bgr,msb,xy       .. file: RDI Acoustic Doppler Current Profiler (ADCP)
b3p,bgr,lsb,xy,prime.. file: Logitech Compress archive data
b8,r,msb,xy,prime   .. file: RDI Acoustic Doppler Current Profiler (ADCP)
b8,g,msb,xy,prime   .. file: RDI Acoustic Doppler Current Profiler (ADCP)
b8,rgb,msb,xy,prime .. file: RDI Acoustic Doppler Current Profiler (ADCP)
b8,bgr,msb,xy,prime .. file: RDI Acoustic Doppler Current Profiler (ADCP)
b8,rgb,msb,yx       .. file: RDI Acoustic Doppler Current Profiler (ADCP)
b8,bgr,msb,yx       .. file: RDI Acoustic Doppler Current Profiler (ADCP)
b8,rgb,msb,yx,prime .. file: RDI Acoustic Doppler Current Profiler (ADCP)
b1,r,msb,XY         .. text: "KXkaojn+b'\t"
b1,r,msb,Xy         .. text: "KXkaojn+b'\t"
b1,r,lsb,xY         .. text: "\t'b+njoakXK"
b1,rgb,msb,Yx       .. file: cpio archive; device 65436, inode 48753, mode 170747, uid 55132, gid 64755, 63431 links, device 0xf75c, modified Mon Jun  9 17:27:03 2053, 2113008583 bytes "\234\337\363_\327\373\034\377\361\235\367\377\035\357\363}\307\367\\367y}\347\373\234\377\371\377\307\177\275\357q\\347\177\235\317\361\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377"                
b1,bgr,msb,Yx       .. file: cpio archive; device 65340, inode 48369, mode 70717, uid 55134, gid 65145, 32199 links, device 0xdf5e, modified Fri Mar 14 06:25:19 2003, 3748755911 bytes ">\367\371_\327{\036\377q?\337\177\037\357y\337\307}^\337s\335\317{>\377\363\377\307\177\275\357q\\317\177=\347\361\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377\377"                                      
b5,r,msb,Yx         .. file: MPEG ADTS, layer II, v1, 48 kHz, Monaural
b5,g,msb,Yx         .. file: MPEG ADTS, layer II, v1, 48 kHz, Monaural
b5,b,msb,Yx         .. file: MPEG ADTS, layer II, v1, 48 kHz, Monaural
b5p,rgb,lsb,Yx      .. file: MPEG ADTS, layer I, v2, Monaural
b5p,bgr,lsb,Yx      .. file: MPEG ADTS, layer I, v2, Monaural
b6,r,msb,Yx         .. file: MPEG ADTS, layer I, v2, 112 kbps, Monaural
b6,g,msb,Yx         .. file: MPEG ADTS, layer I, v2, 112 kbps, Monaural
b6,b,msb,Yx         .. file: MPEG ADTS, layer I, v2, 112 kbps, Monaural
b6,rgb,msb,Yx       .. file: ddis/ddif
b6,bgr,msb,Yx       .. file: ddis/ddif
b7p,rgb,lsb,Yx      .. file: MPEG ADTS, layer II, v1, Monaural
b7p,bgr,lsb,Yx      .. file: MPEG ADTS, layer II, v1, Monaural
b8,r,lsb,Yx         .. file: AIX core file 64-bit
b8,g,lsb,Yx         .. file: AIX core file 64-bit
b1,g,msb,Yx,prime   .. file: Tower/XP rel 3 object
b1,b,lsb,Yx,prime   .. file: OpenPGP Secret Key
b3p,bgr,msb,Yx,prime.. text: "[[_[__[{"
b5p,rgb,lsb,Yx,prime.. file: MPEG ADTS, layer I, v2, 24 kHz, Monaural
b5p,bgr,lsb,Yx,prime.. file: MPEG ADTS, layer I, v2, 24 kHz, Monaural
b6,r,msb,Yx,prime   .. file: MPEG ADTS, layer I, v2, 112 kbps, Monaural
b6,g,msb,Yx,prime   .. file: MPEG ADTS, layer I, v2, 112 kbps, Monaural
b6,b,msb,Yx,prime   .. file: MPEG ADTS, layer I, v2, Monaural
b6,rgb,msb,Yx,prime .. file: ddis/ddif
b6,bgr,msb,Yx,prime .. file: ddis/ddif
b7p,rgb,lsb,Yx,prime.. file: MPEG ADTS, layer II, v1, Monaural
b7p,bgr,lsb,Yx,prime.. file: MPEG ADTS, layer II, v1, Monaural
```
Observation: the LSBs of RGB channels contain hidden data.

---
## Step 2: Extract LSB bytes
```python3
We can extract LSBs from each RGB pixel and pack them into bytes using Python.
The script solution.py accomplishes this.
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
```
Output : 
```bash
payload length: 30
FOUND with wordlist key: Nein b'CGLITCHERS{st3g_1n_th3_p1x3ls}'
```
