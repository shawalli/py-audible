
import audiobook
import os
from binascii import hexlify, unhexlify

audible_dir = "C:\Users\shawalli\Downloads"
aax = os.path.join(audible_dir, "OldMansWarUnabridged_ep6_AH3CF5679N6SR.aax")
print aax

ab = audiobook.Audiobook(aax)