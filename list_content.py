"""
Group 11 - CS632P-Python Programming
Author: XI ZHOU
Author: ALEX ONEILL
Author:
Author:
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


def sizeConvert(size):  # change unit
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


def list_drives(drive):
    # todo how does this work for mac?
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

            # todo do we need to sum the immediate directories and files or all sub files and directories?
            for lists in os.listdir(path):
                sub_path = os.path.join(path, lists)
                # print(sub_path)
                if os.path.isfile(sub_path):
                    filenum = filenum + 1
                elif os.path.isdir(sub_path):
                    dirnum = dirnum + 1
            print('The total number of directories is:', dirnum)
            print('The total number of files is:', filenum)


# MAIN PROGRAM LOGIC
def main():
    parser = argparse.ArgumentParser(add_help=False,
                                     description="""This python application scans the contents of your drive and \
                                     outputs various details based on the input you provide. The output will be \
                                     written to a log file for viewing on demand and sharing as necessary.""")
    # HELP FUNCTION
    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                        help='displays this screen and provides information on what options are available for use')

    # MUTUALLY EXCLUSIVE QUIET AND VERBOSE MODES
    me_group = parser.add_mutually_exclusive_group()
    me_group.add_argument('-v', '--verbose', action='store_true')
    me_group.add_argument('-q', '--quiet', action='store_true')

    parser.add_argument('-d', '--drv', help='lists drive details for the drive letter that is entered', nargs='?',
                        const=string.ascii_uppercase)  # DEFAULT TO ALL DRIVES IF -d IS CALLED BUT NOT SPECIFIED
    parser.add_argument('-l', '--fld', help='lists folder details for all folders in the path that is entered')
    parser.add_argument('-f', '--fil', help='lists file details for all files in the path that is entered')
    parser.add_argument('-t', '--typ', help='lists file type details for the "file type" that is entered')

    args = parser.parse_args()

    # todo -v -q verbose/quiet
    if args.verbose:
        print('in verbose')
    elif args.quiet:
        print('in quiet')
    else:
        print('in standard print')

    # todo -d drive info
    if args.drv:
        print('in drv')
        list_drives(args.drv)
    else:
        print('not using drv')

    # todo -l folders in drive
    if args.fld:
        print('in fld')
    else:
        print('not using fld')

    # todo -f file name matching
    # todo is this supposed to accept a file name to search for?
    if args.fil:
        print('in fil')
    else:
        print('not using fil')

    # todo -t all matches of file type
    if args.typ:
        print('in typ')
    else:
        print('not using typ')


if __name__ == '__main__':
    main()
