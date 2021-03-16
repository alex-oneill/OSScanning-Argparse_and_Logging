"""

Author: XI ZHOU
Author: ALEX ONEILL

Version update: 2021.3.5
Version : 0.85
NOTE: need to wrap it up with argparse

Version update: 2021.3.9
Version : 1
NOTE: finished project with requirements

"""
import os
import pathlib
import shutil
import string
import time
import argparse
import logging
import textwrap
from pathlib import Path


def sizeConvert(size):
    K, M, G = 1024, 1024 ** 2, 1024 ** 3
    if size >= G:
        size = format(size / G, '.2f')
        return str(size) + ' G Bytes'
    elif size >= M:
        size = format(size / M, '.2f')
        return str(size) + ' M Bytes'
    elif size >= K:
        size = format(size / K, '.2f')
        return str(size) + ' K Bytes'
    else:
        return str(size) + ' Bytes'


def list_drives(drive):
    if os.name == 'posix':
        list_drives_mac()
    else:
        list_drives_win(drive)


def list_drives_win(drive=string.ascii_uppercase):
    logging.info('#' * 50)
    logging.info('-drv: This will take a while please wait.')
    drive = drive
    for each_drive in drive:
        if os.path.exists(each_drive + ":\\"):
            path = each_drive + ":\\"
            usage = shutil.disk_usage(path)
            dirnum = 0
            filenum = 0
            logging.info('#' * 50)
            logging.info('Drives total size: {}'.format(sizeConvert(usage.total)))
            logging.info('Drives used size: {}'.format(sizeConvert(usage.used)))
            logging.info('Drives free size: {}'.format(sizeConvert(usage.free)))
            logging.debug('counting files and directories now please wait.')
            for root, dirs, files in os.walk(path):
                try:
                    for file in files:
                        filepath = os.path.join(root, file)
                        if os.path.isfile(filepath):
                            filenum += 1
                    for dir in dirs:
                        dirpath = os.path.join(root, dir)
                        if os.path.isdir(dirpath):
                            dirnum += 1
                except FileNotFoundError as fnf:
                    logging.warning('{} not found {}'.format(path, fnf))
                except OSError as ose:
                    logging.critical('Cannot access {} .Probably a permissions error {}'.format(path, ose))
            logging.info('The total number of directories is: {}'.format(dirnum))
            logging.info('The total number of files is: {}'.format(filenum))


def list_drives_mac(drive="/Volumes"):
    logging.info('#' * 50)
    logging.info('-fld')
    drive = drive
    usage = shutil.disk_usage(drive)
    dirnum = 0
    filenum = 0
    logging.info('In Drive {}'.format(drive))
    logging.info('Drives total size: {}'.format(sizeConvert(usage.total)))
    logging.info('Drives used size: {}'.format(sizeConvert(usage.used)))
    logging.info('Drives free size: {}'.format(sizeConvert(usage.free)))
    logging.debug('counting files and directories now please wait.')
    to_iterate_drive = drive + "/Macintosh HD"
    for root, dirs, files in os.walk(to_iterate_drive):
        try:
            for file in files:
                filepath = os.path.join(root, file)        
                if os.path.isfile(filepath):
                    filenum += 1
            for dir in dirs:
                dirpath = os.path.join(root, dir)
                if os.path.isdir(dirpath):
                    dirnum += 1
        except FileNotFoundError as fnf:
            logging.warning('{} not found {}'.format(drive, fnf))
        except OSError as ose:
            logging.critical('Cannot access {} .Probably a permissions error {}'.format(drive, ose))
    logging.info('The total number of directories is: {}'.format(dirnum))
    logging.info('The total number of files is: {}'.format(filenum))


def get_folder_info(dir):
    logging.info('#' * 50)
    logging.info('-fld')
    if os.path.exists(dir):
        total_size = sum(f.stat().st_size for f in Path(dir).glob('**/*') if f.is_file())
        for item in os.listdir(dir):
            itempath = os.path.join(dir, item)
            try:
                if os.path.isfile(itempath):
                    continue
                elif os.path.isdir(itempath):
                    filenum = len(os.listdir(itempath))
                    root_directory = Path(itempath)
                    filesize = sum(f.stat().st_size for f in root_directory.glob('**/*') if f.is_file())
                    logging.info('folder: {:20}, number of files: {:4}, folder size: {},'.format(itempath, filenum,
                                                                                                 sizeConvert(filesize)))
            except FileNotFoundError as fnf:
                logging.warning('{} not found {}'.format(itempath, fnf))
            except OSError as ose:
                logging.critical('Cannot access {} .Probably a permissions error {}'.format(itempath, ose))
        t_s_format = sizeConvert(total_size)
        logging.info('Total Storage of all files: ' + t_s_format)
    else:
        logging.warning('{} is not a valid path'.format(dir))


def get_all_files(fil):
    if os.name == 'posix':
        get_all_files_mac(fil)
    else:
        get_all_files_win(fil)


def get_all_files_mac(fil):
    logging.info('#' * 50)
    logging.debug('-fil: This will take a while please wait.')
    
    drive = "/Volumes/Macintosh HD"
    if fil == 'all':
        for each_drive in drive:
            if os.path.exists(drive + each_drive):
                dir = drive + each_drive
                try:
                    for root, dirs, files in os.walk(dir):
                        for file in files:
                            filepath = os.path.join(root, file)
                            if os.path.isfile(filepath):
                                filename = file
                                filetype = os.path.splitext(file)[1]
                                filesize = sizeConvert(os.stat(filepath).st_size)
                                filetime = time.strftime('%Y-%m-%d %H:%M:%S',
                                                         time.localtime(os.stat(filepath).st_ctime))
                                logging.info(
                                    'filename: {:30}, filetype: {:7} filesize: {:10}, time stamp: {}'.format(filename,
                                                                                                             filetype,
                                                                                                             filesize,
                                                                                                             filetime))
                except FileNotFoundError as fnf:
                    logging.warning('{} not found {}'.format(dir, fnf))
                except OSError as ose:
                    logging.critical('Cannot access {} .Probably a permissions error {}'.format(dir, ose))

    else:
        found_file = False
        for each_drive in drive:
            if os.path.exists(drive + each_drive):
                dir = drive + each_drive
                for root, dirs, files in os.walk(dir):
                    for file in files:
                        filepath = os.path.join(root, file)
                        if os.path.isfile(filepath):
                            filename = file
                            filetype = os.path.splitext(file)[1]
                            filesize = sizeConvert(os.stat(filepath).st_size)
                            filetime = time.strftime('%Y-%m-%d %H:%M:%S',
                                                     time.localtime(os.stat(fil).st_ctime))
                            if filename.lower() == fil.lower():
                                found_file = True
                                logging.info('File found at path: {}'.format(filepath))
                                logging.info(
                                    'filename: {:30}, filetype: {:7} filesize: {:10}, time stamp: {}'.format(filename,
                                                                                                             filetype,
                                                                                                             filesize,
                                                                                                             filetime))
        if not found_file:
            logging.warning('Unable to find file: {}'.format(fil))


def get_all_files_win(fil):
    logging.info('#' * 50)
    logging.debug('-fil: This will take a while please wait.')
    drive = string.ascii_uppercase
    if fil == 'all':
        for each_drive in drive:
            if os.path.exists(each_drive + ":\\"):
                dir = each_drive + ":\\"
                try:
                    for root, dirs, files in os.walk(dir):
                        for file in files:
                            filepath = os.path.join(root, file)
                            if os.path.isfile(filepath):
                                filename = file
                                filetype = os.path.splitext(file)[1]
                                filesize = sizeConvert(os.stat(filepath).st_size)
                                filetime = time.strftime('%Y-%m-%d %H:%M:%S',
                                                         time.localtime(os.stat(filepath).st_ctime))
                                logging.info(
                                    'filename: {:30}, filetype: {:7} filesize: {:10}, time stamp: {}'.format(filename,
                                                                                                             filetype,
                                                                                                             filesize,
                                                                                                             filetime))
                except FileNotFoundError as fnf:
                    logging.warning('{} not found {}'.format(dir, fnf))
                except OSError as ose:
                    logging.critical('Cannot access {} .Probably a permissions error {}'.format(dir, ose))

    else:
        found_file = False
        for each_drive in drive:
            if os.path.exists(each_drive + ":\\"):
                dir = each_drive + ":\\"
                for root, dirs, files in os.walk(dir):
                    for file in files:
                        filepath = os.path.join(root, file)
                        if os.path.isfile(filepath):
                            filename = file
                            filetype = os.path.splitext(file)[1]
                            filesize = sizeConvert(os.stat(filepath).st_size)
                            filetime = time.strftime('%Y-%m-%d %H:%M:%S',
                                                     time.localtime(os.stat(filepath).st_ctime))
                            if filename.lower() == fil.lower():
                                found_file = True
                                logging.info('File found at path: {}'.format(filepath))
                                logging.info(
                                    'filename: {:30}, filetype: {:7} filesize: {:10}, time stamp: {}'.format(filename,
                                                                                                             filetype,
                                                                                                             filesize,
                                                                                                             filetime))
        if not found_file:
            logging.warning('Unable to find file: {}'.format(fil))


def get_all_types(typ):

    if os.name == 'posix':
        everything_mac(typ)
    else:
        everything_win(typ)


def everything_mac(typ):
    logging.info('#' * 50)
    logging.info('-typ: This will take a while please wait.')
    drive = "/Volumes/Macintosh HD/Users"
    type_dicts = {}
    for each_drive in drive:
        if os.path.exists(drive + each_drive):
            path = drive + each_drive
            for root, dirs, files in os.walk(path):
                for file in files:
                    filepath = os.path.join(root, file)
                    type = os.path.splitext(file)[-1].lower()
                    size = os.stat(filepath).st_size
                    if type in type_dicts.keys():
                        type_dicts[type]['file_count'] += 1
                        type_dicts[type]['total_size'] = type_dicts[type]['total_size'] + size
                    else:
                        type_dicts[type] = {'file_count': 1, 'total_size': size}

    sorted_tups = sorted(type_dicts.items())

    if typ == 'everything':
        for ft in sorted_tups:
            file_count = dict(ft[1])['file_count']
            total_size = sizeConvert(dict(ft[1])['total_size'])
            logging.info(
                'Type: {:10}, File-Count: {}, Total-Size: {}'.format(ft[0], file_count, total_size))
    else:
        if typ[0] != '.':
            typ = '.' + typ
        for ft in sorted_tups:
            if ft[0] == typ:
                file_count = dict(ft[1])['file_count']
                total_size = sizeConvert(dict(ft[1])['total_size'])
                logging.info(
                    'Type: {:10}, File-Count: {}, Total-Size: {}'.format(ft[0], file_count, total_size))


def everything_win(typ):
    logging.info('#' * 50)
    logging.info('-typ: This will take a while please wait.')
    drive = string.ascii_uppercase
    type_dicts = {}
    for each_drive in drive:
        if os.path.exists(each_drive + ":\\"):
            path = each_drive + ":\\"
            for root, dirs, files in os.walk(path):
                for file in files:
                    filepath = os.path.join(root, file)
                    type = os.path.splitext(file)[-1].lower()
                    size = os.stat(filepath).st_size
                    if type in type_dicts.keys():
                        type_dicts[type]['file_count'] += 1
                        type_dicts[type]['total_size'] = type_dicts[type]['total_size'] + size
                    else:
                        type_dicts[type] = {'file_count': 1, 'total_size': size}

    sorted_tups = sorted(type_dicts.items())

    if typ == 'everything':
        for ft in sorted_tups:
            file_count = dict(ft[1])['file_count']
            total_size = sizeConvert(dict(ft[1])['total_size'])
            logging.info('Type: {:10}, File-Count: {}, Total-Size: {}'.format(ft[0], file_count, total_size))
    else:
        if typ[0] != '.':
            typ = '.' + typ
        for ft in sorted_tups:
            if ft[0] == typ:
                file_count = dict(ft[1])['file_count']
                total_size = sizeConvert(dict(ft[1])['total_size'])
                logging.info('Type: {:10}, File-Count: {}, Total-Size: {}'.format(ft[0], file_count, total_size))


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s >>> %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='info.log'
                    )


def main():
    parser = argparse.ArgumentParser(
        add_help=False,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
                    Here is the description of this app
                    *-------------------------------------------------------------*
                        A Python app that will read the contents of any computer,
                        and produce an output based on the input provided.
                        The output will be written into a logging/logger log file,
                        for a view on demand and verification.
                        All the lines of the log file are accompanied by time stamps,
                        along with level message.
                    *-------------------------------------------------------------*
                    '''))

    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                        help='displays this screen and provides information on what options are available for use')
    me_group = parser.add_mutually_exclusive_group()
    me_group.add_argument('-v', '--verbose', action='store_true')
    me_group.add_argument('-q', '--quiet', action='store_true')
    parser.add_argument('-d', '--drv',
                        help='lists drive details for the drive letter that is entered, eg: -l C:',
                        nargs='?', const=string.ascii_uppercase)
    parser.add_argument('-l', '--fld',
                        help='lists folder details for all folders in the path that is entered, eg: -l C:',
                        nargs='?')
    parser.add_argument('-f', '--fil',
                        help='lists file details for all files in the path that is entered, eg: -f C:\\path\\file',
                        nargs='?', const='all')
    parser.add_argument('-t', '--typ', help='lists file type details for the "file type" that is entered, eg: -t exe',
                        nargs='?', const='everything')
    args = parser.parse_args()

    # VERBOSE MODE
    if args.verbose:
        if not any([args.drv, args.fld, args.fil, args.typ]):
            print('No arguments entered -- please enter an argument')
        else:
            console = logging.StreamHandler()
            console.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s >>> %(message)s')
            console.setFormatter(formatter)
            logging.getLogger().addHandler(console)

            if args.drv:
                temppath = args.drv[0].upper()+":"
                if args.drv == 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                    list_drives(args.drv)
                    print('Job completed in verbose mode, please check info.log for details')
                elif os.path.exists(temppath):
                    list_drives(args.drv[0].upper())
                    print('Job completed in verbose mode, please check info.log for details')
                else:
                    print('Please enter a valid drive!')
                    exit()
            if args.fld:
                get_folder_info(args.fld)
                print('Job completed in verbose mode, please check info.log for details')
            if args.fil:
                if args.fil == 'all':
                    start = ''
                    print('\nALERT: Are you sure you want to run -f with no parameters?')
                    print('ALERT: This has the potential to log over 1M lines!')
                    print('ALERT: Consider passing a parameter to search for. Ex) "-f my_doc.txt"')
                    print('\nALERT: To exit and pass a parameter, please enter "N".')
                    print('ALERT: To continue with no parameters, enter "Y".')
                    start = input('Entry: ')
                    if start in ['y', 'Y', 'yes', 'Yes', 'YES']:
                        get_all_files(args.fil)
                        print('Job completed in verbose mode, please check info.log for details')
                else:
                    get_all_files(args.fil)
                    print('Job completed in verbose mode, please check info.log for details')

            if args.typ:
                if args.typ == 'everything':
                    start = ''
                    print('\nALERT: Are you sure you want to run -t with no parameters?')
                    print('ALERT: This has the potential to log over 1M lines!')
                    print('ALERT: Consider passing a parameter to search for. Ex) "-t pdf"')
                    print('\nALERT: To exit and pass a parameter, please enter "N".')
                    print('ALERT: To continue with no parameters, enter "Y".')
                    start = input('Entry: ')
                    if start in ['y', 'Y', 'yes', 'Yes', 'YES']:
                        get_all_types(args.typ)
                        print('Job completed in verbose mode, please check info.log for details')
                else:
                    get_all_types(args.typ)
                    print('Job completed in verbose mode, please check info.log for details')

    # DEFAULT MODE OR QUIET MODE
    else:
        if not any([args.drv, args.fld, args.fil, args.typ]):
            print('No arguments entered -- please enter an argument')

        if args.drv:
            temppath = args.drv[0].upper() + ":"
            if args.drv == 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                list_drives(args.drv)
                print('Job completed in quiet mode, please check info.log for details')
            elif os.path.exists(temppath):
                list_drives(args.drv[0].upper())
                print('Job completed in quiet mode, please check info.log for details')
            else:
                print('Please enter a valid drive!')
                exit()
        if args.fld:
            get_folder_info(args.fld)
            print('Job completed in quiet mode, please check info.log for details')
        if args.fil:
            if args.fil == 'all':
                start = ''
                print('\nALERT: Are you sure you want to run -f with no parameters?')
                print('ALERT: This has the potential to log over 1M lines!')
                print('ALERT: Consider passing a parameter to search for. Ex) "-f my_doc.txt"')
                print('\nALERT: To exit and pass a parameter, please enter "N".')
                print('ALERT: To continue with no parameters, enter "Y".')
                start = input('Entry: ')
                if start in ['y', 'Y', 'yes', 'Yes', 'YES']:
                    get_all_files(args.fil)
                    print('Job completed in verbose mode, please check info.log for details')
            else:
                get_all_files(args.fil)
                print('Job completed in quiet mode, please check info.log for details')

        if args.typ:
            if args.typ == 'everything':
                start = ''
                print('\nALERT: Are you sure you want to run -t with no parameters?')
                print('ALERT: This has the potential to log over 1M lines!')
                print('ALERT: Consider passing a parameter to search for. Ex) "-t pdf"')
                print('\nALERT: To exit and pass a parameter, please enter "N".')
                print('ALERT: To continue with no parameters, enter "Y".')
                start = input('Entry: ')
                if start in ['y', 'Y', 'yes', 'Yes', 'YES']:
                    get_all_types(args.typ)
                    print('Job completed in quiet mode, please check info.log for details')
            else:
                get_all_types(args.typ)
                print('Job completed in quiet mode, please check info.log for details')


if __name__ == '__main__':
    main()
