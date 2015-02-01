
import audiobook
import os
from binascii import hexlify, unhexlify
import avconv

audible_dir = "C:\Users\shawalli\Downloads"
aax = os.path.join(audible_dir, "OldMansWarUnabridged_ep6_AH3CF5679N6SR.aax")
print aax

ab = audiobook.Audiobook(aax)
ab.seek(0)
# for i in range(18):
    # print 'CHAPTER %d' % i
    # ch_info = ab._dll.AAXGetChapterInfo(ab._audiobook_handle, i)
    # print repr(ch_info)
    # print
# print
# print
# print
# for i in range(100):
    # frame_info = ab._dll.AAXGetNextFrameInfo(ab._audiobook_handle)
    # enc_buf, length = ab._dll.AAXGetEncodedAudio(ab._audiobook_handle, 0x400)
    # print 'FRAME'
    # print repr(frame_info)
    # print 'ENC_BUF: length: %d (%x)' % (length, length)
    # # print buf.raw
    # print

def chapter_one_iter():
    sample_rate = ab._dll.AAXGetSampleRate(ab._audiobook_handle)
    channels = ab._dll.AAXGetAudioChannelCount(ab._audiobook_handle)
    frame_width = sample_rate * channels

    ch1_info = ab._dll.AAXGetChapterInfo(ab._audiobook_handle, 0)
    ch2_info = ab._dll.AAXGetChapterInfo(ab._audiobook_handle, 1)
    print 'CHAPTER 1'
    print repr(ch1_info)
    print repr(ch2_info)
    
    num_frames = 0
    frame = ''
    frame_bytes = 0
    total_enc_len = 0
    while True:
        frame_info = ab._dll.AAXGetNextFrameInfo(ab._audiobook_handle)
        if frame_info is None:
            print 'ERR'
            break
        if frame_info.start_time_milli >= ch2_info.start_time_milli:
            print 'LAST FRAME',
            print '%x  %x ... %x' % (frame_info.start_time_milli, frame_info.encoded_frame_data_length, ch2_info.start_time_milli)
            # print repr(frame_info)
            break
        
        num_frames += 1
        print '%d   %x/%x' % (num_frames, frame_info.start_time_milli, ch2_info.start_time_milli), repr(frame_info)
        (enc_buf, enc_len) = ab._dll.AAXGetEncodedAudio(ab._audiobook_handle, 0x400)
        total_enc_len += enc_len
        (dec_buf, dec_len) = ab._dll.AAXDecodePCMFrame(ab._audiobook_handle, enc_buf, enc_len, (frame_width - frame_bytes))
        frame += dec_buf.raw[:dec_len]
        frame_bytes += dec_len
        
        if (frame_width - frame_bytes) < 4096:
            yield frame
            frame = ''
            frame_bytes = 0

    if frame_bytes > 0:
        yield frame
    print "DONE"

av = avconv.AvConv('old2.mp3', *'-f s16le -ac 2 -ar 22050 -i -'.split(' '))
for frame in chapter_one_iter():
    av.write(frame)
av.close()