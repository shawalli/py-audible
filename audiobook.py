
import os
import audible

DEFAULT_AUDIOBOOK_DIRECTORY = "C:\\Users\\Public\\Documents\\Audible\\Downloads"

# UNIX_AUDIBLE_DLL = '/usr/share/audible/bin/AAXSDKWin.dll'
# UNIX_AUDIOBOOK_DIR = os.path.join(os.getenv('HOME', default), 'Downloads')

class Audiobook:
    def __init__(self, filepath):
        if os.path.exists(filepath) is False:
            filepath = os.path.join(DEFAULT_AUDIOBOOK_DIRECTORY, filepath)
            print 'Audiobook does not exist at \'%s\'; trying default directory' % filepath
            if os.path.exists(filepath) is False:
                raise OSError('Audiobook could not be found')

        self._filepath = filepath
        
        self._dll = audible.AudibleDll(UNIX_AUDIBLE_DLL)
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
    
    def _decode_book_iter(self):
        self._dll.AAXSeek(self._audiobook_handle, 0)
        # self._dll.AAXSeekToChapter(self._audiobook_handle, 17)
        
        sample_rate = self._dll.AAXGetSampleRate(self._audiobook_handle)
        channels = self._dll.AAXGetChapterCount(self._audiobook_handle)
        
        frame_width = sample_rate * channels
        frame = ''
        frame_bytes = 0
        
        frame_info = self._dll.AAXGetNextFrameInfo(self._audiobook_handle)
        while frame_info is not None:
            (buf, length) = self._dll.AAXGetEncodedAudio(self._audiobook_handle, 0x400)
            (decoded_buf, decoded_buf_length) = self._dll.AAXDecodePCMFrame(self._audiobook_handle, buf, length, (frame_width - frame_bytes))
            frame += buf.raw[:decoded_buf_length]
            frame_bytes += decoded_buf_length
            
            if frame_width - frame_bytes < 4096:
                yield frame
                frame = ''
                frame_bytes = 0
                
        if frame_bytes > 0:
            yield frame
#     
#     def decode_book(self):
