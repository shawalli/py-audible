
import audible
import os

dll = audible.AudibleDll("C:\Program Files (x86)\Audible\Bin\AAXSDKWin.dll")

audible_dir = "C:\Users\Public\Documents\Audible\Downloads"
aax = os.path.join(audible_dir, "OldMansWar_ep6_AH3CF5679N6SR.aax")
# audible_dir = "C:\Users\shawalli\Downloads"
# aax = os.path.join(audible_dir, "OldMansWarUnabridged_ep6_AH3CF5679N6SR.aax")
print aax
print 'Opening File'
handle = dll.AAXOpenFileWinW(aax)
print handle

print 'DRM'
print dll.AAXGetDRMType(handle)
print 'authenticating'
print dll.AAXAuthenticateWin(handle)

print 'getting channels'
print dll.AAXGetAudioChannelCount(handle)
print 'getting sample rate'
print dll.AAXGetSampleRate(handle)
print 'seeking'
dll.AAXSeek(handle,0)

print 'getting audio'
(buf, length) = dll.AAXGetEncodedAudio(handle, 0x400);
print buf
print length

dll.AAXCloseFile(handle)

