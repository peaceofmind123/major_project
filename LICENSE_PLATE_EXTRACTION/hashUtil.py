# Copyright Ashish Paudel 2019, all rights reserved.
import hashlib
import os
import sys
import hexdump


def hash_file(filename):
    try:
        with open(filename, 'rb') as data:
            data_hex = hexdump.hexdump(data, result='return').encode('utf-8')
            digest = hashlib.md5(bytearray(data_hex))

            os.rename(filename, os.path.join(
                os.path.dirname(filename), f'{digest.hexdigest()}.png'))
    except FileNotFoundError as e:
        print(e)


def hash_multiple_files(dirname):
    for filename in os.listdir(dirname):
        hash_file(os.path.abspath(os.path.join(dirname, filename)))


# use python3 hashUtil.py images for our use case
if __name__ == '__main__':
    if sys.argv[1] is None:
        print('requires positional argument "dirname"')
        exit()

    dirname = os.path.abspath(os.path.join(
        os.path.dirname(sys.argv[0]), sys.argv[1]))
    print(dirname)
    hash_multiple_files(dirname)
