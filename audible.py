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
	
	def _load_AAXOpenFileWinW(self):
		func_name = 'AAXOpenFileWinW'
		f = self._handle[func_name]
		f.argtypes = [POINTER(POINTER(c_ubyte)), wintypes.LPWSTR]
		
		setattr(self._handle_funcs, func_name, f)

	def AAXOpenFileWinW(self, aax_filename):
		aax_handle = POINTER(c_ubyte)()
		print aax_handle
		fname_buf = wintypes.LPWSTR(aax_filename)
		print fname_buf
		
		returnCode = self._handle_funcs.AAXOpenFileWinW(byref(aax_handle), fname_buf)
		self._checkFuncResult(returnCode, 'AAXOpenFileWinW')
		
		return aax_handle
	
	# def AAXCloseFile(self, aax_handle):
		