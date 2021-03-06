
import os
import audible
import avconv

DEFAULT_AUDIOBOOK_DIRECTORY = "C:\\Users\\Public\\Documents\\Audible\\Downloads"

# UNIX_AUDIBLE_DLL = '/usr/share/audible/bin/AAXSDKWin.dll'
# UNIX_AUDIOBOOK_DIR = os.path.join(os.getenv('HOME', default), 'Downloads')

class AudiobookException(Exception): pass

class Audiobook:
    """
    todo:
    - extract picture, set as class attribute
    - attach picture to each chapter
    - extract title
    - attach title as prefix for filename of each chapter
    - convert mp3 to m4b
    - add relevant ID3Tag info (Author, disc x/y, length of chapter, etc
    """
    def __init__(self, filepath):
        if os.path.exists(filepath) is False:
            filepath = os.path.join(DEFAULT_AUDIOBOOK_DIRECTORY, filepath)
            print 'Audiobook does not exist at \'%s\'; trying default directory' % filepath
            if os.path.exists(filepath) is False:
                raise OSError('Audiobook could not be found')

        self._filepath = filepath
        
        self._dll = audible.AudibleDll()
        self._audiobook_handle = None
        self._open()
        from binascii import hexlify

        self._authenticate()
        self._channels = self._dll.AAXGetAudioChannelCount(self._audiobook_handle)
        self._sample_rate = self._dll.AAXGetSampleRate(self._audiobook_handle)
        self._frame_width = self._channels * self._sample_rate
    
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        self._close()
        self._dll = None
    
    def _authenticate(self):
        try:
            self._dll.AAXAuthenticateWin(self._audiobook_handle)
        except DllReturnCodeError:
            raise Exception('Authentication error; trying logging in from AudibleManager first')

    def _open(self):
        if self._audiobook_handle is not None:
            return
        self._audiobook_handle = self._dll.AAXOpenFileWinA(self._filepath)
    
    def _close(self):
        if self._audiobook_handle is None:
            return
        self._dll.AAXCloseFile(self._audiobook_handle)
        self._audiobook_handle = None
    
    def seek(self, offset):
        self._dll.AAXSeek(self._audiobook_handle, offset)
    
    def seek_to_chapter(self, book_chapter):
        chapter = self._book_chapter_to_dll_chapter(book_chapter)
        self._dll.AAXSeekToChapter(self._audiobook_handle, chapter)

    def get_chapter_count(self):
        chapters = self._dll.AAXGetChapterCount(self._audiobook_handle)
        return chapters
    
    def _get_ffmpeg_args(self):
        args = \
        [
            '-f',
            's16le',
            '-ac',
            str(self._channels),
            '-ar',
            str(self._sample_rate),
            '-i',
            '-'
        ]
        return args
    
    def chapter_to_mp3(self, book_chapter):
        filename='oldmanswar_%d.mp3' % book_chapter
        
        av = avconv.AvConv(filename, *self._get_ffmpeg_args())
        for frame in self._decode_chapter_iter(book_chapter):
            av.write(frame)
        av.close()
        return filename
    
    @staticmethod
    def _book_chapter_to_dll_chapter(book_chapter):
        return book_chapter - 1
    
    def _verify_chapter(self, book_chapter):
        chapter_count = self.get_chapter_count()
        if book_chapter > chapter_count:
            raise IndexError('Chapter out of bounds (%d chapters)' % chapter_count)
    
    def _decode_chapter_iter(self, book_chapter):
        # For some reason, the handle needs to be reset before it can perform certain DLL functions
        self.seek(0)
        
        self._verify_chapter(book_chapter)
        chapter = self._book_chapter_to_dll_chapter(book_chapter)
        
        if book_chapter == self.get_chapter_count():
            next_ch_info = None
        else:
            next_ch_info = self._dll.AAXGetChapterInfo(self._audiobook_handle, chapter+1)
        
        self.seek_to_chapter(book_chapter)
        
        frame = ''
        frame_bytes = 0
        while True:
            frame_info = self._dll.AAXGetNextFrameInfo(self._audiobook_handle)
            if frame_info is None:
                if next_ch_info is not None:
                    raise AudiobookException('Error pulling frame for chapter')
                break
            
            # if on the last chapter, continue until frame_info is returned as None
            if next_ch_info is not None:
                if frame_info.start_time_milli >= next_ch_info.start_time_milli:
                    break
                
            
            (enc_buf, enc_len) = self._dll.AAXGetEncodedAudio(self._audiobook_handle)
            (dec_buf, dec_len) = self._dll.AAXDecodePCMFrame(self._audiobook_handle, enc_buf, enc_len, (self._frame_width - frame_bytes))
            frame += dec_buf.raw[:dec_len]
            frame_bytes += dec_len
            
            if (self._frame_width - frame_bytes) < audible.AudibleDll.PCM_BUFFER_SIZE:
                yield frame
                frame = ''
                frame_bytes = 0

        if frame_bytes > 0:
            yield frame
    
    def _decode_book_iter(self):
        self._dll.AAXSeek(self._audiobook_handle, 0)
    
        frame = ''
        frame_bytes = 0
        while True:
            frame_info = self._dll.AAXGetNextFrameInfo(self._audiobook_handle)
            if frame_info is None:
                break
            
            (enc_buf, enc_len) = self._dll.AAXGetEncodedAudio(self._audiobook_handle)
            (dec_buf, dec_len) = self._dll.AAXDecodePCMFrame(self._audiobook_handle, enc_buf, enc_len, (self._frame_width - frame_bytes))
            frame += dec_buf.raw[:dec_len]
            frame_bytes += dec_len
            
            if (self._frame_width - frame_bytes) < audible.AudibleDll.PCM_BUFFER_SIZE:
                yield frame
                frame = ''
                frame_bytes = 0

        if frame_bytes > 0:
            yield frame
    
    def book_to_mp3(self, output_filepath):
        av = avconv.AvConv(output_filepath, *self._get_ffmpeg_args())
        for frame in self._decode_book_iter():
            av.write(frame)
        av.close()
        return output_filepath