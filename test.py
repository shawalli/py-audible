
import audible
import os
from binascii import hexlify, unhexlify

audible_dir = "C:\Users\shawalli\Downloads"
aax = os.path.join(audible_dir, "OldMansWarUnabridged_ep6_AH3CF5679N6SR.aax")
print aax

# dll = audible.AudibleDll("C:\Program Files (x86)\Audible\Bin\AAXSDKWin.dll")

# audible_dir = "C:\Users\Public\Documents\Audible\Downloads"
# aax = os.path.join(audible_dir, "OldMansWar_ep6_AH3CF5679N6SR.aax")
# print 'Opening File'
# handle = dll.AAXOpenFileWinW(aax)
# print handle

# print 'DRM'
# print dll.AAXGetDRMType(handle)
# print 'authenticating'
# print dll.AAXAuthenticateWin(handle)

# print 'getting channels'
# print dll.AAXGetAudioChannelCount(handle)
# print 'getting sample rate'
# print dll.AAXGetSampleRate(handle)
# print 'seeking'
# dll.AAXSeek(handle,0)
# print 'chapters'
# print dll.AAXGetChapterCount(handle)
# c = []
# for i in range(18):
	# # c.append(dll.AAXGetChapterStartTime(handle, i))
	# c.append(dll.AAXGetChapterInfo(handle, i).raw)
# import struct
# for ch in c:
	# # print '%08x' % struct.unpack_from('<I', ch)
	# print '%08x%08x%08x%08x%08x' % struct.unpack_from('<5I', ch),
	# print '%02x%02x%02x' % struct.unpack_from('<3B', ch, offset=19)

# print 'getting audio'
# (buf, length) = dll.AAXGetEncodedAudio(handle, 0x400);
# print buf
# print length

# dll.AAXCloseFile(handle)

ab = audible.Audiobook(aax)
ab.dummy()
# (buf, length) = ab.get_chapter_encoded_audio(1)
# print length