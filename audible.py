#!c:/Python/python.exe
import os
from ctypes import *
from ctypes import wintypes
from UserDict import UserDict


DEFAULT_DLL_DIRECTORY = "C:\\Program Files (x86)\\Audible\Bin"
DEFAULT_DLL_FILENAME = "AAXSDKWin.dll"

DEFAULT_AUDIOBOOK_DIRECTORY = "C:\\Users\\Public\\Documents\\Audible\\Downloads"

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
			'AAXOpenFileWinW',
			[POINTER(POINTER(c_ubyte)), wintypes.LPWSTR])
			
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
	
	def AAXOpenFileWinW(self, file_path):
		aax_handle = POINTER(c_ubyte)()
		fname_buf = wintypes.LPWSTR(file_path)
		
		returnCode = self._handle_funcs.AAXOpenFileWinW(byref(aax_handle), fname_buf)
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

class Audiobook:
	def __init__(self, filepath):
		if os.path.exists(filepath) is False:
			filepath = os.path.join(DEFAULT_AUDIOBOOK_DIRECTORY, filepath)
			print 'Audiobook does not exist at \'%s\'; trying default directory' % filepath
			if os.path.exists(filepath) is False:
				raise OSError('Audiobook could not be found')

		self._filepath = filepath
		
		self._dll = AudibleDll()
		self._audiobook_handle = None
		self.open()
		self._authenticate()
		# import struct
		# for i in range(1,18):
			# print i
			# c = self._dll.AAXGetChapterInfo(self._audiobook_handle, i)
			# print '%08x%08x%08x%08x%08x' % struct.unpack_from('<5I',c.raw),
			# print '%x%x%x' % struct.unpack_from('<3B', c.raw, offset=20)

	def _verify_opened(self):
		if self._audiobook_handle is None:
			raise ValueError('Operation on closed audiobook')

	def _authenticate(self):
		try:
			self._dll.AAXAuthenticateWin(self._audiobook_handle)
		except DllReturnCodeError:
			raise Exception('Authentication error; trying logging in from AudibleManager first')

	def _get_chapter_offset(self, chapter):
		offset = 0
		
		for i in range(0, (chapter - 1)):
			offset += self._dll.AAXGetChapterStartTime(self._audiobook_handle, chapter)
		return offset
	
	# def _get_chapter_length(self, chapter):
		
	
	def open(self):
		if self._audiobook_handle is not None:
			return
		self._audiobook_handle = self._dll.AAXOpenFileWinW(self._filepath)
	
	def close(self):
		if self._audiobook_handle is None:
			return
		self._dll.AAXCloseFile(self._audiobook_handle)
		self._audiobook_handle = None
	
	def seek(self, offset):
		self._verify_opened()
		self._dll.AAXSeek(self._audiobook_handle, offset)

	def get_chapter_count(self):
		self._verify_opened()
		chapters = self._dll.AAXGetChapterCount(self._audiobook_handle)
		return chapters.value

	def get_chapter_encoded_audio(self, book_chapter):
		chapter_count = self.get_chapter_count()
		if book_chapter > chapter_count:
			raise IndexError('Chapter out of bounds (%d chapters)' % chapter_count)
		# change from 1-indexed (book chapters start at 1) to 0-indexed (arrays start at 0)
		chapter = book_chapter - 1
		
		offset = self._get_chapter_offset(chapter)
		length = self._dll.AAXGetChapterStartTime(self._audiobook_handle, chapter)
		print 'off: len'
		print offset, length
		
		self._dll.AAXSeek(self._audiobook_handle, offset)
		return self._dll.AAXGetEncodedAudio(self._audiobook_handle, length)
	
	def dummy(self):
		self._dll.AAXSeek(self._audiobook_handle, 0)
		# self._dll.AAXSeekToChapter(self._audiobook_handle, 17)
		length = 1
		overall_length = 0
		while (length > 0):
			(buf, length) = self._dll.AAXGetEncodedAudio(self._audiobook_handle, 0x400)
			overall_length += length
			print '%x,  %x' % (length,overall_length)
