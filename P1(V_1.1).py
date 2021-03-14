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
import shutil
import string
import time
import argparse
import logging
import sys
import textwrap
from pathlib import Path


def sizeConvert(size):  # change unit
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


def list_drives(drive=string.ascii_uppercase):
	drive = drive
	for each_drive in drive:
		if os.path.exists(each_drive + ":\\"):
			path = each_drive + ":\\"
			# print('-' * 50)
			# print('In Drive', path)
			usage = shutil.disk_usage(path)
			# print('Drives total size:', sizeConvert(usage.total))
			# print('Drives used size:', sizeConvert(usage.used))
			# print('Drives free size:', sizeConvert(usage.free))
			# print('counting files and directories now please wait.')
			dirnum = 0
			filenum = 0
			logging.info('#' * 50)
			logging.info('In Drive {}'.format(path))
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
				except OSError as ose:
					# print('Cannot access ' + path + '. Probably a permissions error ', ose)
					logging.critical('Cannot access {} .Probably a permissions error {}'.format(path, ose))
				except FileNotFoundError as fnf:
					# print(path + ' not found ', fnf)
					logging.warning('{} not found {}'.format(path, fnf))
			# print('The total number of directories is:', dirnum)
			# print('The total number of files is:', filenum)
			logging.info('The total number of directories is: {}'.format(dirnum))
			logging.info('The total number of files is: {}'.format(filenum))


def list_drives_ml(path):
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

		
def get_folder_info(DIR):
	if os.path.exists(DIR):
		total_size = sum(f.stat().st_size for f in Path(DIR).glob('**/*') if f.is_file())
		for item in os.listdir(DIR):
			itempath = os.path.join(DIR, item)
			try:
				if os.path.isfile(itempath):
					continue
				elif os.path.isdir(itempath):
					filenum = len(os.listdir(itempath))
					root_directory = Path(itempath)
					filesize = sum(f.stat().st_size for f in root_directory.glob('**/*') if f.is_file())
					# print('folder: {:20}, number of files: {:4}, folder size: {},'.format(itempath, filenum,
					# 																	  sizeConvert(filesize)))
					logging.info('folder: {:20}, number of files: {:4}, folder size: {},'.format(itempath, filenum,
					                                                                             sizeConvert(filesize)))
			except OSError as ose:
				# print('Cannot access ' + itempath + '. Probably a permissions error ', ose)
				logging.critical('Cannot access {} .Probably a permissions error {}'.format(itempath, ose))
			except FileNotFoundError as fnf:
				# print(itempath + ' not found ', fnf)
				logging.warning('{} not found {}'.format(itempath, fnf))
		t_s_format = sizeConvert(total_size)
		# print('Total Storage of all files: ', t_s_format)
		logging.info('Total Storage of all files: ' + t_s_format)
	else:
		# print('Invalid path!')
		logging.warning('{} is not a valid path'.format(DIR))


def get_all_files(fil='all'):
	# print('This will take a while please wait.')
	logging.debug('This will take a while please wait.')
	drive = string.ascii_uppercase
	if fil == 'all':
		for each_drive in drive:
			if os.path.exists(each_drive + ":\\"):
				DIR = each_drive + ":\\"
				try:
					for root, dirs, files in os.walk(DIR):
						for file in files:
							filepath = os.path.join(root, file)
							if os.path.isfile(filepath):
								filename = file
								filetype = os.path.splitext(file)[1]
								filesize = sizeConvert(os.stat(filepath).st_size)
								filetime = time.strftime('%Y-%m-%d %H:%M:%S',
								                         time.localtime(os.stat(filepath).st_ctime))
								# print('filename: {:30}, filetype: {:7} filesize: {:10}, time stamp: {}'.format(filename,
								# 																			   filetype,
								# 																			   filesize,
								# 																			   filetime))
								logging.info(
									'filename: {:30}, filetype: {:7} filesize: {:10}, time stamp: {}'.format(filename,
									                                                                         filetype,
									                                                                         filesize,
									                                                                         filetime))
				except OSError as ose:
					# print('Cannot access ' + DIR + '. Probably a permissions error ', ose)
					logging.critical('Cannot access {} .Probably a permissions error {}'.format(DIR, ose))
				except FileNotFoundError as fnf:
					# print(DIR + ' not found ', fnf)
					logging.warning('{} not found {}'.format(DIR, fnf))
	else:
		if os.path.exists(fil):
			head, tail = os.path.split(fil)
			if os.path.isfile(fil):
				filename = tail
				filetype = os.path.splitext(tail)[1]
				filesize = sizeConvert(os.stat(fil).st_size)
				filetime = time.strftime('%Y-%m-%d %H:%M:%S',
				                         time.localtime(os.stat(fil).st_ctime))
				# print('filename: {:30}, filetype: {:7} filesize: {:10}, time stamp: {}'.format(filename,
				# 																			   filetype,
				# 																			   filesize,
				# 																			   filetime))
				logging.info(
					'filename: {:30}, filetype: {:7} filesize: {:10}, time stamp: {}'.format(filename,
					                                                                         filetype,
					                                                                         filesize,
					                                                                         filetime))
		else:
			logging.warning('{} is not a valid file path'.format(fil))


def get_all_types(typ='all'):
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
	drive = string.ascii_uppercase
	for each_drive in drive:
		if os.path.exists(each_drive + ":\\"):
			path = each_drive + ":\\"
			try:
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
			except OSError as ose:
				# print('Cannot access ' + path + '. Probably a permissions error ', ose)
				logging.critical('Cannot access {} .Probably a permissions error {}'.format(path, ose))
			except FileNotFoundError as fnf:
				# print(path + ' not found ', fnf)
				logging.warning('{} not found {}'.format(path, fnf))
	# print('This will take a while please wait.')
	if typ == 'all':
		# print('Number of type .py files is {:10d}, total size is {}'.format(py_file_num, sizeConvert(py_file_size)))
		# print(
		# 	'Number of type .ipynb files is {:10d}, total size is {}'.format(ipynb_file_num, sizeConvert(ipynb_file_size)))
		# print('Number of type .exe files is {:10d}, total size is {}'.format(exe_file_num, sizeConvert(exe_file_size)))
		# print('Number of type .txt files is {:10d}, total size is {}'.format(txt_file_num, sizeConvert(txt_file_size)))
		# print('Number of type .csv files is {:10d}, total size is {}'.format(csv_file_num, sizeConvert(csv_file_size)))
		# print('Number of type .pdf files is {:10d}, total size is {}'.format(pdf_file_num, sizeConvert(pdf_file_size)))
		# print('Number of other type files is {:10d}, total size is {}'.format(other_file_num, sizeConvert(other_file_size)))
		logging.info('This will take a while please wait.')
		logging.info(
			'Number of type .py files is {:10d}, total size is {}'.format(py_file_num, sizeConvert(py_file_size)))
		logging.info(
			'Number of type .ipynb files is {:10d}, total size is {}'.format(ipynb_file_num,
			                                                                 sizeConvert(ipynb_file_size)))
		logging.info(
			'Number of type .exe files is {:10d}, total size is {}'.format(exe_file_num, sizeConvert(exe_file_size)))
		logging.info(
			'Number of type .txt files is {:10d}, total size is {}'.format(txt_file_num, sizeConvert(txt_file_size)))
		logging.info(
			'Number of type .csv files is {:10d}, total size is {}'.format(csv_file_num, sizeConvert(csv_file_size)))
		logging.info(
			'Number of type .pdf files is {:10d}, total size is {}'.format(pdf_file_num, sizeConvert(pdf_file_size)))
		logging.info(
			'Number of other type files is {:10d}, total size is {}'.format(other_file_num,
			                                                                sizeConvert(other_file_size)))
	elif typ == 'py':
		logging.info(
			'Number of type .py files is {:10d}, total size is {}'.format(py_file_num, sizeConvert(py_file_size)))
	elif typ == 'ipynb':
		logging.info(
			'Number of type .ipynb files is {:10d}, total size is {}'.format(ipynb_file_num,
			                                                                 sizeConvert(ipynb_file_size)))
	elif typ == 'exe':
		logging.info(
			'Number of type .exe files is {:10d}, total size is {}'.format(exe_file_num, sizeConvert(exe_file_size)))
	elif typ == 'txt':
		logging.info(
			'Number of type .txt files is {:10d}, total size is {}'.format(txt_file_num, sizeConvert(txt_file_size)))
	elif typ == 'csv':
		logging.info(
			'Number of type .csv files is {:10d}, total size is {}'.format(csv_file_num, sizeConvert(csv_file_size)))
	elif typ == 'pdf':
		logging.info(
			'Number of type .pdf files is {:10d}, total size is {}'.format(pdf_file_num, sizeConvert(pdf_file_size)))
	elif typ == 'other':
		logging.info(
			'Number of other type files is {:10d}, total size is {}'.format(other_file_num,
			                                                                sizeConvert(other_file_size)))
	else:
		logging.warning('unable to recognize this format')


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s >>> %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='info.log'
                    )


def main():
	parser = argparse.ArgumentParser(
		add_help=False,
		prog='l_c',
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
	parser.add_argument('-d', '--drv', help='lists drive details for the drive letter that is entered, eg: -l C:',
	                    nargs='?')  # DEFAULT TO ALL DRIVES IF -d IS CALLED BUT NOT SPECIFIED
	parser.add_argument('-l', '--fld',
	                    help='lists folder details for all folders in the path that is entered, eg: -l C:',
	                    nargs='?')
	parser.add_argument('-f', '--fil', help='lists file details for all files in the path that is entered, eg: -f C:\\path\\file',
	                    nargs='?')
	parser.add_argument('-t', '--typ', help='lists file type details for the "file type" that is entered, eg: -t exe',
	                    nargs='?')
	args = parser.parse_args()
	
	Osys = os.name # OSYS = nt for windows and posix for unix

	if args.verbose:
		print('in verbose mode')
		console = logging.StreamHandler()
		console.setLevel(logging.INFO)
		formatter = logging.Formatter('%(asctime)s - %(levelname)s >>> %(message)s')
		console.setFormatter(formatter)
		logging.getLogger().addHandler(console)
		if sys.argv[2] == '-d':
			if Osys == ("posix"):
				list_drives_ml(sys.argv[3])
			else:
				list_drives(sys.argv[3])
		elif sys.argv[2] == '-l':
			get_folder_info(sys.argv[3])
		elif sys.argv[2] == '-f':
			get_all_files(sys.argv[3])
		elif sys.argv[2] == '-t':
			get_all_types(sys.argv[3])
	elif args.quiet:
		print('in quiet mode')
		if sys.argv[2] == '-d':
			print('in drv')
			if Osys == ("posix"):
				list_drives_ml(sys.argv[3])
			else:
				list_drives(sys.argv[3])
			print('job finished please check the file info.log')
		elif sys.argv[2] == '-l':
			get_folder_info(sys.argv[3])
			print('job finished please check the file info.log')
		elif sys.argv[2] == '-f':
			get_all_files(sys.argv[3])
			print('job finished please check the file info.log')
		elif sys.argv[2] == '-t':
			get_all_types(sys.argv[3])
			print('job finished please check the file info.log')
	else:
		print('please use the right syntax')


if __name__ == '__main__':
	main()
