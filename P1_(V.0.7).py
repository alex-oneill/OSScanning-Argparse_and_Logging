"""
Author: XI ZHOU
Version : 0.7
Date: 2021.3.3

TODO: wrap with argparse and logging

"""

import os
import shutil
import string
import time
from pathlib import Path


def sizeConvert(size):  # change unit
	K, M, G = 1024, 1024 ** 2, 1024 ** 3
	if size >= G:
		size = format(size / G, '.4f')
		return str(size) + ' G Bytes'
	elif size >= M:
		size = format(size / M, '.4f')
		return str(size) + ' M Bytes'
	elif size >= K:
		size = format(size / K, '.4f')
		return str(size) + ' K Bytes'
	else:
		return str(size) + ' Bytes'


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
			print('folder: {}, file num: {}, folder size: {},'.format(itempath, filenum, a))
	
	return total_size


# print("Total Size: " + str(get_folder_info(DIR)))


def get_all_files(DIR):
	for item in os.listdir(DIR):
		itempath = os.path.join(DIR, item)
		if os.path.isfile(itempath):
			filename = item
			filesize = os.stat(itempath).st_size
			filetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.stat(itempath).st_ctime))
			print('filename: {}, filesize: {}, filetime: {}'.format(filename, filesize, filetime))
		
		elif os.path.isdir(itempath):
			a = get_all_files(itempath)
			if None != a:
				print(a)


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
	
	print('Number of type .py files is {:10d}, total size is {}'.format(py_file_num, sizeConvert(py_file_size)))
	print(
		'Number of type .ipynb files is {:10d}, total size is {}'.format(ipynb_file_num, sizeConvert(ipynb_file_size)))
	print('Number of type .exe files is {:10d}, total size is {}'.format(exe_file_num, sizeConvert(exe_file_size)))
	print('Number of type .txt files is {:10d}, total size is {}'.format(txt_file_num, sizeConvert(txt_file_size)))
	print('Number of type .csv files is {:10d}, total size is {}'.format(csv_file_num, sizeConvert(csv_file_size)))
	print('Number of type .pdf files is {:10d}, total size is {}'.format(pdf_file_num, sizeConvert(pdf_file_size)))
	print('Number of other type files is {:10d}, total size is {}'.format(other_file_num, sizeConvert(other_file_size)))
