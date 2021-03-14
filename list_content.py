"""
Group 11 - CS632P-Python Programming
Author: XI ZHOU
Author: ALEX ONEILL
Author: SAAHIIL MESWAANII
Author:
"""

import argparse
import logging
import os
import shutil
import string
import time
from pathlib import Path

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

def func_dir(path):
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
Osys = os.name # OSYS = nt for windows and posix for unix
if Osys == ("posix"):

    def list_drives(path):
        path1 = os.getcwd()
        #print(path)
        for file in os.listdir("/Volumes"):
            total, used, free = shutil.disk_usage("/Volumes/" + file)
            print('-' * 50)
            print("Name of Drive: ",file)
            used = total - free
            print('Drives total size:', sizeConvert(total))
            print('Drives used size:', sizeConvert(used))
            print('Drives free size:', sizeConvert(free))
            func_dir(path1)
        
else:
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
                
                func_dir(path)



def get_folder_info(DIR):
    total_size = sum(f.stat().st_size for f in Path(DIR).glob('**/*') if f.is_file())
    for item in os.listdir(DIR):
        itempath = os.path.join(DIR, item)
        if os.path.isfile(itempath):
            continue

        elif os.path.isdir(itempath):
            filenum = len(os.listdir(itempath))
            root_directory = Path(itempath)
            a = sum(f.stat().st_size for f in root_directory.glob('**/*') if f.is_file())
            print('folder: {}\tfile num: {}\tfolder size: {}'.format(itempath, filenum, sizeConvert(a)))


# todo DO WE WANT FULL FOLDER RECURSION ON THIS? OR JUST LEVEL 0?
def get_all_files(DIR):
    for item in os.listdir(DIR):
        itempath = os.path.join(DIR, item)
        if os.path.isfile(itempath):
            filename = item
            filesize = os.stat(itempath).st_size
            filetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.stat(itempath).st_ctime))
            print('filename: {}, filesize: {}, filetime: {}'.format(filename, sizeConvert(filesize), filetime))

        elif os.path.isdir(itempath):
            a = get_all_files(itempath)
            if None != a:
                print(a)


# todo DO WE WANT FULL FOLDER RECURSION ON THIS? OR JUST LEVEL 0?
def get_all_types(path):
    py_file_num = 0
    py_file_size = 0
    ipynb_file_num = 0
    ipynb_file_size = 0
    exe_file_num = 0
    exe_file_size = 0
    txt_file_num = 0
    txt_file_size = 0
    csv_file_num = 0
    csv_file_size = 0
    pdf_file_num = 0
    pdf_file_size = 0
    other_file_num = 0
    other_file_size = 0

    for root, dirs, files in os.walk(path):
        for file in files:
            filepath = os.path.join(root, file)
            if os.path.splitext(file)[-1] == '.py':
                py_file_num += 1
                py_file_size += os.stat(filepath).st_size
            elif os.path.splitext(file)[-1] == '.ipynb':
                ipynb_file_num += 1
                ipynb_file_size += os.stat(filepath).st_size
            elif os.path.splitext(file)[-1] == '.exe':
                exe_file_num += 1
                exe_file_size += os.stat(filepath).st_size
            elif os.path.splitext(file)[-1] == '.txt':
                txt_file_num += 1
                txt_file_size += os.stat(filepath).st_size
            elif os.path.splitext(file)[-1] == '.csv':
                csv_file_num += 1
                csv_file_size += os.stat(filepath).st_size
            elif os.path.splitext(file)[-1] == '.pdf':
                pdf_file_num += 1
                pdf_file_size += os.stat(filepath).st_size
            else:
                other_file_num += 1
                other_file_size += os.stat(filepath).st_size

    print('Number of type .py files is: {:<5d}\ttotal size is {}'.format(py_file_num, sizeConvert(py_file_size)))
    print(
        'Number of type .ipynb files is: {:<5d}\ttotal size is {}'.format(ipynb_file_num, sizeConvert(ipynb_file_size)))
    print('Number of type .exe files is: {:<5d}\ttotal size is {}'.format(exe_file_num, sizeConvert(exe_file_size)))
    print('Number of type .txt files is: {:<5d}\ttotal size is {}'.format(txt_file_num, sizeConvert(txt_file_size)))
    print('Number of type .csv files is: {:<5d}\ttotal size is {}'.format(csv_file_num, sizeConvert(csv_file_size)))
    print('Number of type .pdf files is: {:<5d}\ttotal size is {}'.format(pdf_file_num, sizeConvert(pdf_file_size)))
    print('Number of other type files is: {:<5d}\ttotal size is {}'.format(other_file_num, sizeConvert(other_file_size)))


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

    # GET DRIVE INFO
    if args.drv:
        # print('in drv')
        list_drives(args.drv)
    # else:
        # print('not using drv')

    # GET FOLDER INFO
    if args.fld:
        # print('in fld')
        get_folder_info(args.fld)
    # else:
    #     print('not using fld')

    # GET FILE INFO
    if args.fil:
        # print('in fil')
        get_all_files(args.fil)
    # else:
    #     print('not using fil')

    # GET FILE TYPE INFO
    if args.typ:
        # print('in typ')
        get_all_types(args.typ)
    # else:
    #     print('not using typ')


if __name__ == '__main__':
    main()
