
import audiobook
import os
from binascii import hexlify, unhexlify
import struct

audible_dir = "C:\Users\shawalli\Downloads"
aax = os.path.join(audible_dir, "OldMansWarUnabridged_ep6_AH3CF5679N6SR.aax")
print aax

ab = audiobook.Audiobook(aax)
ab.seek(0)
for i in range(18):
    print 'CHAPTER %d' % i
    ch_info = ab._dll.AAXGetChapterInfo(ab._audiobook_handle, i)
    print repr(ch_info)
    # print '%08x %08x %08x %08x %08x %08x' % struct.unpack_from('<6I', ch_info.raw)
    print
print
print
print
for i in range(100):
    frame_info = ab._dll.AAXGetNextFrameInfo(ab._audiobook_handle)
    enc_buf, length = ab._dll.AAXGetEncodedAudio(ab._audiobook_handle, 0x400)
    print 'FRAME'
    print repr(frame_info)
    # print '%08x %08x %08x %08x %08x %08x' % struct.unpack_from('<6I', frame_info.raw)
    print 'ENC_BUF: length: %d (%x)' % (length, length)
    # print buf.raw
    print