#!c:/Python/python.exe
import os
from ctypes import *
from ctypes import wintypes
from UserDict import UserDict


DEFAULT_DLL_DIRECTORY = "C:\\Program Files (x86)\\Audible\Bin"
DEFAULT_DLL_FILENAME = "AAXSDKWin.dll"

class DllReturnCodeError(Exception):
    def __init__(self, returnCode):
        returnCode = str(returnCode)
        Exception.__init__(self, returnCode)

class AudibleDll(object):
    def __init__(self, filepath=None):
        if filepath is None:
            parentDir = DEFAULT_DLL_DIRECTORY
            filename = DEFAULT_DLL_FILENAME
            filepath = os.path.join(parentDir, filename)
        
        if os.path.exists(filepath) is False:
            raise OSError('AAX Library does not exist at \'%s\'' % filepath)

        (self._parentDir, self._filename) = os.path.split(filepath)
        os.environ['PATH'] = ';'.join([os.environ['PATH'], self._parentDir])
        
        self._handle = CDLL(self._filename)
        
        self._loadDllFunctions()

    def _loadDllFunction(self, func_name, func_args):
        f = self._handle[func_name]
        f.argtypes = func_args[:]
        setattr(self._handle_funcs, func_name, f)
        
    def _loadDllFunctions(self):
        self._handle_funcs = UserDict()
        
        self._loadDllFunction(
            'AAXOpenFileWinA',
            [POINTER(POINTER(c_ubyte)), POINTER(c_char)])
            
        self._loadDllFunction(
            'AAXCloseFile',
            [POINTER(c_ubyte)])
            
        self._loadDllFunction(
            'AAXAuthenticateWin',
            [POINTER(c_ubyte)])
            
        self._loadDllFunction(
            'AAXGetDRMType',
            [POINTER(c_ubyte), POINTER(c_int)])
            
        self._loadDllFunction(
            'AAXSeek',
            [POINTER(c_ubyte), c_int])
            
        self._loadDllFunction(
            'AAXSeekToChapter',
            [POINTER(c_ubyte), c_int])
            
        self._loadDllFunction(
            'AAXGetAudioChannelCount',
            [POINTER(c_ubyte), POINTER(wintypes.DWORD)])
            
        self._loadDllFunction(
            'AAXGetChapterCount',
            [POINTER(c_ubyte), POINTER(wintypes.DWORD)])
            
        self._loadDllFunction(
            'AAXGetChapterInfo',
            [POINTER(c_ubyte), c_uint, POINTER(c_char)])
            
        self._loadDllFunction(
            'AAXGetChapterStartTime',
            [POINTER(c_ubyte), c_uint, POINTER(wintypes.DWORD)])
            
        self._loadDllFunction(
            'AAXGetSampleRate',
            [POINTER(c_ubyte), POINTER(wintypes.DWORD)])
            
        self._loadDllFunction(
            'AAXGetEncodedAudio',
            [POINTER(c_ubyte), POINTER(c_char), wintypes.DWORD, POINTER(wintypes.DWORD)])
    
        self._loadDllFunction(
            'AAXGetNextFrameInfo',
            [POINTER(c_ubyte), POINTER(c_char)])
        
        self._loadDllFunction(
            'AAXDecodePCMFrame',
            [POINTER(c_ubyte), POINTER(c_char), wintypes.DWORD, POINTER(c_char), wintypes.DWORD, POINTER(wintypes.DWORD)])
    
    def AAXOpenFileWinA(self, file_path):
        aax_handle = POINTER(c_ubyte)()
        # fname_buf = wintypes.LPWSTR(file_path)
        fname_buf = create_string_buffer(file_path)
        
        returnCode = self._handle_funcs.AAXOpenFileWinA(byref(aax_handle), fname_buf)
        if returnCode != 0:
            raise DllReturnCodeError(returnCode)
        return aax_handle
    
    def AAXCloseFile(self, aax_handle):
        returnCode = self._handle_funcs.AAXCloseFile(aax_handle)
        if returnCode != 0:
            raise DllReturnCodeError(returnCode)

    def AAXAuthenticateWin(self, aax_handle):
        returnCode = self._handle_funcs.AAXAuthenticateWin(aax_handle)
        if returnCode != 0:
            raise DllReturnCodeError(returnCode)

    def AAXGetDRMType(self, aax_handle):
        drm_type = c_int()
        
        returnCode = self._handle_funcs.AAXGetDRMType(aax_handle, byref(drm_type))
        if returnCode != 0:
            raise DllReturnCodeError(returnCode)
        return drm_type.value

    def AAXSeek(self, aax_handle, offset):
        offset = c_int(offset)
        returnCode = self._handle_funcs.AAXSeek(aax_handle, offset)
        if returnCode != 0:
            raise DllReturnCodeError(returnCode)

    def AAXSeekToChapter(self, aax_handle, chapter):
        chapter = c_int(chapter)
        returnCode = self._handle_funcs.AAXSeekToChapter(aax_handle, chapter)
        if returnCode != 0:
            raise DllReturnCodeError(returnCode)

    def AAXGetAudioChannelCount(self, aax_handle):
        channels = wintypes.DWORD()
        returnCode = self._handle_funcs.AAXGetAudioChannelCount(aax_handle, byref(channels))
        if returnCode != 0:
            raise DllReturnCodeError(returnCode)
        return channels.value

    def AAXGetChapterCount(self, aax_handle):
        chapters = wintypes.DWORD()
        returnCode = self._handle_funcs.AAXGetChapterCount(aax_handle, byref(chapters))
        if returnCode != 0:
            raise DllReturnCodeError(returnCode)
        return chapters.value

    def AAXGetChapterInfo(self, aax_handle, chapter):
        buf_size = 22
        buf = create_string_buffer(buf_size)
        # buf = cast(create_string_buffer(buf_size), POINTER(wintypes.BYTE))
        chapter = c_uint(chapter)
        
        returnCode = self._handle_funcs.AAXGetChapterInfo(aax_handle, chapter, buf)
        if returnCode != 0:
            raise DllReturnCodeError(returnCode)
        return buf

    def AAXGetChapterMetadata(self, aax_handle, chapter):
        buf_size = 22
        buf = create_string_buffer(buf_size)
        # buf = cast(create_string_buffer(buf_size), POINTER(wintypes.BYTE))
        chapter = c_uint(chapter)
        
        returnCode = self._handle_funcs.AAXGetChapterMetadata(aax_handle, chapter, buf)
        if returnCode != 0:
            raise DllReturnCodeError(returnCode)
        return buf

    def AAXGetChapterStartTime(self, aax_handle, chapter):
        chapter = c_uint(chapter)
        start_time = wintypes.DWORD()
        
        returnCode = self._handle_funcs.AAXGetChapterStartTime(aax_handle, chapter, byref(start_time))
        if returnCode != 0:
            raise DllReturnCodeError(returnCode)
        return start_time.value
    
    def AAXGetSampleRate(self, aax_handle):
        sample_rate = wintypes.DWORD()
        returnCode = self._handle_funcs.AAXGetSampleRate(aax_handle, byref(sample_rate))
        if returnCode != 0:
            raise DllReturnCodeError(returnCode)
        return sample_rate.value

    def AAXGetEncodedAudio(self, aax_handle, buf_size):
        buf = create_string_buffer(buf_size)
        length = wintypes.DWORD()
        
        returnCode = self._handle_funcs.AAXGetEncodedAudio(aax_handle, buf, buf_size, byref(length))
        if returnCode != 0:
            raise DllReturnCodeError(returnCode)
        return (buf, length.value)
    
    def AAXDecodePCMFrame(self, aax_handle, buf, buf_size, bytes_left_in_frame):
        buf_size = wintypes.DWORD(buf_size)
        bytes_left_in_frame = wintypes.DWORD(bytes_left_in_frame)
        decoded_buf = create_string_buffer(0x2000)
        out_size = wintypes.DWORD()
        
        returnCode = self._handle_funcs.AAXDecodePCMFrame(aax_handle, buf, buf_size, decoded_buf, bytes_left_in_frame, byref(out_size))
        if returnCode != 0:
            raise DllReturnCodeError(returnCode)
        return (decoded_buf, out_size.value)
    
    def AAXGetNextFrameInfo(self, aax_handle):
        buf = create_string_buffer(24)
        
        returnCode = self._handle_funcs.AAXGetNextFrameInfo(aax_handle, buf)
        if returnCode != 0:
            if returnCode == -24:
                print 'got 24 err'
                buf = None
            else:
                raise DllReturnCodeError(returnCode)
        return buf