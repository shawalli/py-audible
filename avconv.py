
import subprocess

class AvConv(object):
    def __init__(self, output_file, *args):
        cmd = ['ffmpeg.exe']
        cmd += list(args) + [output_file]
        
        self._process = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    
    def write(self, data):
        self._process.stdin.write(data)
        self._process.stdin.flush()
    
    def close(self):
        self._process.communicate() 