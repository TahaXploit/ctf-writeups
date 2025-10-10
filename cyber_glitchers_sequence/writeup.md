# Cyber Glitchers Sequence Edition CTF Writeup

## Observations

When running the binary, we observed the following outputs:

- `"Welcome to Cyber Glitchers sequence edition!"`  
- `"Enter the correct sequence of numbers..."`  
- `"Wrong for attempt %zu. Decoy: FLAG{fake_flag}"`  
- `"FLAG DECRYPTED:"`  

These messages indicate that the binary performs a **sequence check** followed by a **local decryption routine** if the correct sequence is entered.

---

## Static Analysis with Ghidra

### Import and Initial Analysis

1. Open **Ghidra**.  
2. Create a **New Project** and import the binary (`l3osforavecjuin.exe`).  
3. Run **Auto Analysis** with default options.  

#### Strings of Interest

Search for relevant strings such as:  

- `"FLAG DECRYPTED"`  
- `"Decoy"`  
- `"Attempt"`  

Navigate to **cross-references (XREFs)** to see which functions handle the sequence input and the decryption logic.

**Screenshot suggestion:**  
<img width="1098" height="682" alt="image" src="https://github.com/user-attachments/assets/a5522d00-fd4c-451c-89c0-bbb91bef35d2" />

---

### Decompiled Main Function

The key function handling the logic is `FUN_00101100`.  

Analysis revealed:

- The binary prompts the user for **numbers in the range 1-100**.  
- Each input is compared against a predefined array of numbers (`DAT_0010224c + lVar7 * 4`).  
- Incorrect input triggers a decoy flag: `"FLAG{fake_flag}"`.  
- Correct input leads to a **local decryption routine**:
  - Allocates memory.
  - Performs XOR with a stored blob (`DAT_00104024`).
  - Applies transformations to finally reveal the **real flag**.

<img width="614" height="721" alt="image" src="https://github.com/user-attachments/assets/d1558cd6-b6ca-4e7c-8213-f3e7f4a595a2" />
<img width="792" height="82" alt="image" src="https://github.com/user-attachments/assets/401d3a18-46ce-43f1-a01b-75a054a8fa5f" />


---

### Reverse Engineering Key Details

- Sequence length is verified before decryption.  
- Magic bytes are checked in the blob (`DAT_00104021`, `DAT_00104022`, `DAT_00104023`).  
- The decryption routine uses **XOR and subtraction** to recover the flag.  

<img width="782" height="320" alt="image" src="https://github.com/user-attachments/assets/572d032e-0eda-4fde-8925-d71d28297e1a" />
- `
DWORDs at 00102250.. :
  0x00102250: 0x49 = 73
  0x00102254: 0x25 = 37
  0x00102258: 0x38 = 56
  0x0010225c: 0x0c = 12
  0x00102260: 0x63 = 99
So the program expects these five numbers (in that order):
73, 37, 56, 12, 99`
---

## Flag Extraction

After understanding the sequence and decryption routine in Ghidra:

1. Identify the correct sequence of numbers in the static data section.  
2. Input the numbers in order when prompted by the binary.  
3. The binary prints the decrypted flag:
 We will use a python script to do that :
```bash
# feed_5_numbers.py
import pexpect, sys

sequence = [73, 37, 56, 12, 99]   # the 5 expected DWords you discovered

child = pexpect.spawn('./l3osforavecjuin.exe', timeout=10)
# optional: log all interaction to stdout
child.logfile = sys.stdout.buffer

try:
    for num in sequence:
        # adapt the prompt if your binary uses slightly different text
        child.expect(r'Attempt \d+: enter number \(1-100\):')
        child.sendline(str(num))

    # wait for process to finish or for the flag to appear
    child.expect(pexpect.EOF)
except pexpect.TIMEOUT:
    print("\nTimeout waiting for prompt/EOF. Last buffer:")
    print(child.before.decode(errors='ignore'))
except pexpect.EOF:
    # process ended; child.before contains last output
    pass

# print the whole output we captured (child.logfile already printed it)
out = child.before.decode(errors='ignore')
print("\n--- final output ---\n")
print(out)
```
Output :
```bash
Welcome to Cyber Glitchers sequence edition!
Are you really a good guesser? Let's see... Have fun!
Enter the correct sequence of numbers (each 1-100) in order to decrypt the flag.
Attempt 1: enter number (1-100): 73
73
OK — got attempt 1 right.
Attempt 2: enter number (1-100): 37
37
OK — got attempt 2 right.
Attempt 3: enter number (1-100): 56
56
OK — got attempt 3 right.
Attempt 4: enter number (1-100): 12
12
OK — got attempt 4 right.
Attempt 5: enter number (1-100): 99
99
OK — got attempt 5 right.
Sequence correct — decrypting...
FLAG DECRYPTED: CGLITCHERS{4MIIIIIINEE_1N_DA_H000US33}

--- final output ---

 99
OK — got attempt 5 right.
Sequence correct — decrypting...
FLAG DECRYPTED: CGLITCHERS{4MIIIIIINEE_1N_DA_H000US33}
```
We finally have the flag:
**FLAG DECRYPTED: CGLITCHERS{4MIIIIIINEE_1N_DA_H000US33}**
