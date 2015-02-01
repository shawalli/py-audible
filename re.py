
import audiobook
import os

audible_dir = "C:\Users\shawalli\Downloads"
aax = os.path.join(audible_dir, "OldMansWarUnabridged_ep6_AH3CF5679N6SR.aax")
# print aax

with audiobook.Audiobook(aax) as ab:
    # ab.book_to_mp3()
    for i in range(ab.get_chapter_count()):
        ab.chapter_to_mp3(i+1)