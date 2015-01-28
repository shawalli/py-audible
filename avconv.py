
import os
import subprocess

class AvConv(object):
    def __init__(self, output_file, *args):
        cmd = ['ffmpeg.exe']
        cmd += list(args) + [output_file]
        
        self._process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    def write(self, data):
        self._process.stdin.write(data)
        self._process.stdin.flush()
    
    def close(self):
        self._process.communicate() 

# a = AvConv('old2.mp3', *'-f s16le -ac 2 -ar 22050 -i -'.split(' '))
# f = open('/home/shawalli/git/aa2mp3/decoded.out', 'rb')


# section = None
# while section != '':
    # section = f.read(4096)
    # a.write(section)

# f.close()
# a.close()