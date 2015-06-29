
import audiobook
import os
import sys
from binascii import hexlify, unhexlify
import argparse

def parse_args(args):
    parser = argparse.ArgumentParser(description="Convert an audible audiobook to mp3.")
    parser.add_argument('--audible-book', '-a', metavar='PATH', type=str, dest='input_file', help='Path of audible audiobook to convert.')
    parser.add_argument('--book-name', '-b', metavar='BOOK_NAME', type=str, dest='book_title', help='Name of book title (used in output file naming.')
    parser.add_argument('-o', metavar='PATH', type=str, dest='output_directory', help='Directory path for output file.')
    
    args = parser.parse_args()
    
    return args

def convert(input_file, output_file):
    ab = audiobook.Audiobook(input_file)
    return ab.book_to_mp3(output_file)

def main():
    args = sys.argv
    args = parse_args(args)
    
    input_file = args.input_file
    book_title = args.book_title
    output_dir = args.output_directory
    
    output_file = os.path.join(output_dir, book_title) + '.mp3'
    convert(input_file, output_file)

if __name__ == '__main__':
    main()