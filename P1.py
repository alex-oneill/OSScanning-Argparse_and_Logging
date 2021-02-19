"""
Author: XI ZHOU

"""

import argparse
import logging
import os
import shutil
import string

# delete 'filename = path' to show the log in the console and not save to a file
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(threadName)s - %(message)s',
                    datefmt='%m-%d %H:%M',
                    )


def sizeConvert(size):                                   # change unit
    K, M, G = 1024, 1024**2, 1024**3
    if size >= G:
        size = format(size/G,'.4f')
        return str(size)+' G Bytes'
    elif size >= M:
        size = format(size/M, '.4f')
        return str(size)+' M Bytes'
    elif size >= K:
        size = format(size/K, '.4f')
        return str(size)+' K Bytes'
    else:
        return str(size)+' Bytes'


def list_drives():
    drive = string.ascii_uppercase
    for each_drive in drive:
        if os.path.exists(each_drive + ":\\"):
            path = each_drive + ":\\"
            print('-' * 50)
            print('In Drive', path)
            # logging.info('In Drive '.format(path))
            usage = shutil.disk_usage(path)
            print('Drives total size:', sizeConvert(usage.total))
            print('Drives used size:', sizeConvert(usage.used))
            print('Drives free size:', sizeConvert(usage.free))

            dirnum = 0
            filenum = 0

            for lists in os.listdir(path):
                sub_path = os.path.join(path, lists)
                # print(sub_path)
                if os.path.isfile(sub_path):
                    filenum = filenum + 1
                elif os.path.isdir(sub_path):
                    dirnum = dirnum + 1
            print('The total number of directories is:', dirnum)
            print('The total number of files is:', filenum)

list_drives()


# parser = argparse.ArgumentParser(
#             prog='PROG',
#             formatter_class=argparse.RawDescriptionHelpFormatter,
#             description=textwrap.dedent('''\
#                     Here is the description of this app
#                     ----------------------------------------------------------------
#                         A Python app that will read the contents of any computer,
#                         and produce an output based on the input provided.
#                         The output will be written into a logging/logger log file,
#                         for a view on demand and verification.
#                         All the lines of the log file are accompanied by time stamps,
#                         along with level message'
#                     ****************************************************************
#                     '''))
#  class FooAction(argparse.Action):
#      def __init__(self, option_strings, dest, nargs=None, **kwargs):
#          if nargs is not None:
#              raise ValueError("nargs not allowed")
#          super(FooAction, self).__init__(option_strings, dest, **kwargs)
#      def __call__(self, parser, namespace, values, option_string=None):
#          print('%r %r %r' % (namespace, values, option_string))
#          setattr(namespace, self.dest, values)
#
#  parser = argparse.ArgumentParser()
#  parser.add_argument('--foo', action=FooAction)
#  parser.add_argument('bar', action=FooAction)
#  args = parser.parse_args('1 --foo 2'.split())
#
# emample page https://www.cnblogs.com/piperck/p/8446580.html

# https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.name
# http://yuncode.net/code/c_5c1472793502833 show filetype number
# parser.print_help()