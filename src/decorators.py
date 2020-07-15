from typing import BinaryIO


def offset_error_logger(func):
    def wrapper(file: BinaryIO, *args):
        try:
            return func(file, *args)
        except Exception as ex:
            print('Current file position: ' + hex(file.tell()).upper())
            raise ex
    return wrapper


def read_file_error_logger(func):
    def wrapper(filename):
        try:
            return func(filename)
        except Exception as e:
            print("Failed to read " + filename + ": " + str(e))
    return wrapper
