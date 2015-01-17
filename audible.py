#!c:/Python/python.exe
import os
from ctypes import *
from ctypes import wintypes
from UserDict import UserDict


DEFAULT_DLL_DIRECTORY = "C:\\Program Files (x86)\\Audible\Bin\\AAXSDKWin.dll"
DEFAULT_DLL_FILENAME = "AAXSDKWin.dll"

class AudibleDll(object):
	def __init__(self, filepath=None):
		if filepath is None:
			self._parentDir = DEFAULT_DLL_DIRECTORY
			self._filename = DEFAULT_DLL_FILENAME
			filepath = os.path.join([self._parentDir, self._filename])
		
		if os.path.exists(filepath) is False:
			raise OSError('AAX Library does not exist at \'%s\'' % filepath)

		(self._parentDir, self._filename) = os.path.split(filepath)
		os.environ['PATH'] = ';'.join([os.environ['PATH'], self._parentDir])
		
		self._handle = CDLL(self._filename)
		
		self._loadDllFunctions()
	
	@staticmethod
	def _checkFuncResult(returnCode, funcName, raiseError=False):
		if returnCode != 0:
			msg = '%s return code was %d' % (funcName, returnCode)
			if raiseError is True:
				raise Exception(msg)
			else:
				msg = 'WARNING: ' + msg
				print msg
	
	def _loadDllFunctions(self):
		self._handle_funcs = UserDict()
		
		self._load_AAXOpenFileWinW()
		self._load_AAXCloseFile()
		self._load_AAXAuthenticateWin()
		self._load_AAXSeek()
		self._load_AAXGetAudioChannelCount()
	
	def _loadDllFunction(self, func_name, func_args):
		f = self._handle[func_name]
		f.argtypes = func_args[:]
		setattr(self._handle_funcs, func_name, f)
	
	def _load_AAXOpenFileWinW(self):
		self._loadDllFunction(
			'AAXOpenFileWinW',
			[POINTER(POINTER(c_ubyte)), wintypes.LPWSTR])

	def _load_AAXCloseFile(self):
		self._loadDllFunction(
			'AAXCloseFile',
			[POINTER(c_ubyte)])

	def _load_AAXAuthenticateWin(self):
		self._loadDllFunction(
			'AAXAuthenticateWin',
			[POINTER(c_ubyte)])

	def _load_AAXSeek(self):
		self._loadDllFunction(
			'AAXOpenFileWinW',
			[POINTER(POINTER(c_ubyte)), c_int])

	def _load_AAXGetAudioChannelCount(self):
		self._loadDllFunction(
			'AAXGetAudioChannelCount',
			[POINTER(POINTER(c_ubyte)), POINTER(c_uint)])

	def AAXOpenFileWinW(self, aax_filename):
		aax_handle = POINTER(c_ubyte)()
		fname_buf = wintypes.LPWSTR(aax_filename)
		
		returnCode = self._handle_funcs.AAXOpenFileWinW(byref(aax_handle), fname_buf)
		self._checkFuncResult(returnCode, 'AAXOpenFileWinW')
		
		return (returnCode, aax_handle)
	
	def AAXCloseFile(self, aax_handle):
		returnCode = self._handle_funcs.AAXCloseFile(aax_handle)
		self._checkFuncResult(returnCode, 'AAXCloseFile')
		return (returnCode,)

	def AAXAuthenticateWin(self, aax_handle):
		returnCode = self._handle_funcs.AAXAuthenticateWin(aax_handle)
		self._checkFuncResult(returnCode, 'AAXAuthenticateWin')
		return (returnCode,)

	def AAXSeek(self, aax_handle, offset):
		returnCode = self._handle_funcs.AAXSeek(aax_handle, offset)
		self._checkFuncResult(returnCode, 'AAXSeek')
		return (returnCode,)

	def AAXGetAudioChannelCount(self, aax_handle):
		channels = wintypes.DWORD()
		returnCode = self._handle_funcs.AAXGetAudioChannelCount(aax_handle, byref(channels))
		self._checkFuncResult(returnCode, 'AAXGetAudioChannelCount')
		return (returnCode,channels)