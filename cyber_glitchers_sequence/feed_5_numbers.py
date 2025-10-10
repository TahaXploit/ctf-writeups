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
