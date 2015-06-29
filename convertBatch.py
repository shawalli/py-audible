
import audiobook
import os
import sys
from binascii import hexlify, unhexlify
import argparse

def parse_args(args):
    parser = argparse.ArgumentParser(description="Convert all audible audiobooks found in a directory to mp3.")
    parser.add_argument('--input-dir', '-i', metavar='PATH', type=str, dest='input_dir', help='Path of audible books directory.', required=True)
    parser.add_argument('--output-dir', '-o', metavar='PATH', type=str, dest='output_dir', help='Path of output directory.', required=True)
    
    args = parser.parse_args()
    
    return args
    
def convert(input_file, output_dir):
    parent_dir, input_filename = os.path.split(input_file)
    output_filename = input_filename.split('_', 1)[0]
    
    output_file = os.path.join(output_dir, output_filename) + '.mp3'
    
    ab = audiobook.Audiobook(input_file)
    return ab.book_to_mp3(output_file)

def batch_convert(input_dir, output_dir):
    input_files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
    
    for f in input_files:
        convert(f, output_dir)

def main():
    args = sys.argv
    args = parse_args(args)
    
    batch_convert(args.input_dir, args.output_dir)

if __name__ == '__main__':
    main()