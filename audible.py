
import os
import ctypes

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
		
		self._handle = ctypes.CDLL(self._filename)
		self.AAXOpenFileWinW = self._handle['AAXOpenFileWinW']

	# def load