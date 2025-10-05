# 🧠 CTF Write-Up: Hidden Secrets (Steganography Challenge)

**Category:** Steganography  
**Difficulty:** Very Easy  
**Flag Format:** `CGLITCHERS{...}`  

---

## 📝 Challenge Description

> Some secrets are not meant to be found… unless you know where to look.  
> We’ve hidden a sensitive file inside an innocent-looking image. The file is a ZIP archive containing the flag, but it’s locked with a password.

🎯 **Goal:**  
Extract the hidden ZIP file from the image, crack the password, and retrieve the flag.

---

## 🔍 Step 1 – Inspect the image

Since the challenge mentioned a hidden file, I used **binwalk** to check for embedded data:

```bash
binwalk -e CGLITCHERS.png
```
Output :
```bash
DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
20488         0x5008          Zip archive data, encrypted at least v2.0 to extract, compressed size: 76, uncompressed size: 70, name: fakeflag.txt
20650         0x50AA          Zip archive data, encrypted at least v2.0 to extract, compressed size: 193, uncompressed size: 222, name: secret.txt

WARNING: One or more files failed to extract: either no utility was found or it's unimplemented
```
🧩 Observation: There’s a ZIP file embedded inside the PNG. We will use 20488.


## 🧰 Step 2 – Extract Hidden Files

I used binwalk’s --dd flag to automatically extract all embedded data.
```bash
IMG="CGLITCHERS.png"
dd if="$IMG" of=zip_20488.zip bs=1 skip=20488 status=progress                                                                                       
```
Output:
```bash
623+0 records in
623+0 records out
623 bytes copied, 0.00158508 s, 393 kB/s
```
✅ The zip_20488.zip file appeared in the CGLITCHERS.png.extracted directory.

## 🔐 Step 3 – Crack the ZIP Password
When trying to unzip the file, it asked for a password.
```bash
unzip -l zip_20488.zip
```
Output:
```bash
Archive:  zip_20488.zip
  Length      Date    Time    Name
---------  ---------- -----   ----
       70  2025-09-30 12:18   fakeflag.txt
      222  2025-09-30 12:16   secret.txt
---------                     -------
      292                     2 files
```
Let’s use fcrackzip with the rockyou.txt wordlist to brute-force it.
```bash
fcrackzip -v -u -D -p /usr/share/wordlists/rockyou.txt zip_20488.zip
```
Output :
```bash
found file 'fakeflag.txt', (size cp/uc     76/    70, flags 9, chk 3a4a)
found file 'secret.txt', (size cp/uc    193/   222, flags 9, chk 3a0e)


PASSWORD FOUND!!!!: pw == loveme
```

## 📂 Step 4 – Extract the Flag
Now unzip it with the found password:
```bash
unzip -P 'loveme' zip_20488.zip
```
Output:
```bash
Archive:  zip_20488.zip
  inflating: fakeflag.txt            
  inflating: secret.txt              
     
```
Check the flag:
```bash
cat secret.txt  
```
Output:
```text
here's your flag 


CGLITCHERS{HE3_1AF44444444A3_QHQ33}


You’re one step ahead… the secret is hidden in a very old and simple substitution where letters trade places with their twins on the other side of the alphabet
```

## 🔡 Step 5 – Decode the hidden message
The challenge hint said:
> “The secret is hidden in a very old and simple substitution where letters trade places with their twins on the other side of the alphabet.”

This indicates a ROT13 cipher (13-letter substitution).

Decoded using ROT13:

> CGLITCHERS{UR3_1NS44444444N3_DUD33}

## 💡 Key Takeaways
- Learned to use binwalk for steganography analysis.

- Practiced ZIP password cracking with fcrackzip.

- Applied a ROT13 substitution cipher for decryption.

- Strengthened analytical and step-by-step investigation skills.
