from time import strftime, strptime
import fileinput
import shutil
import os
import datetime
import platform
import settings


def get_path(req_file):
    if len(req_file) == 0:
        req_file = input('Which file do you want to archive: ')
    path_to_file = os.path.abspath(req_file)
    return path_to_file


def modification_date(path_to_file):
    time = os.path.getmtime(path_to_file)
    stamp = datetime.datetime.fromtimestamp(time)
    return datetime.date.strftime(stamp, '-%m-%d-%Y')


def creation_date(path_to_file):
    if platform.system() == 'Windows':
        print('this is from a Windows machine')
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            print('this is from a Mac machine')
            return stat.st_birthtime
        except AttributeError:
            print('this is from neither Windows or Mac')
            return strftime('-%m-%d-%Y')


select_report = str(2)    # input('\nSelect report to archive:\n - CAPRS_V1.csv = 1\n - rpt_open_CAPRS.csv = 2\n - test.csv = 3\n')
if select_report == str(1):
    if settings.system == 'mac':
        begin_path = (settings.base+'reports/CAPRS_V1.csv')
    elif settings.system == 'windows':
        begin_path = (settings.base+'reports\\CAPRS_V1.csv')
if select_report == str(2):
    if settings.system == 'mac':
        begin_path = (settings.base+'reports/rpt_open_CAPRS.csv')
    elif settings.system == 'windows':
        begin_path = (settings.base+'reports\\rpt_open_CAPRS.csv')
if select_report == str(3):
    if settings.system == 'mac':
        begin_path = (settings.base+'reports/test.csv')
    elif settings.system == 'windows':
        begin_path = (settings.base+'reports\\test.csv')


# TO-DO: write an else statement to handle incorrect entries


path_to_file = get_path(begin_path)
base = os.path.basename(path_to_file)
file = os.path.splitext(base)
head, tail = os.path.splitext(path_to_file)
arch_date = modification_date(path_to_file)
arch_path = head+tail
head = os.path.split(begin_path)
arch_path_supplement = '/archive/'
new_arch = head[0]+arch_path_supplement+file[0]+arch_date+tail
print('arch_path', arch_path, '\nnew_arch', new_arch)


# if select_report == str(1):
#     try:
#         shutil.move(arch_path, new_arch)
#     except:
#         print('Could not archive the old CAPRS_V1.csv file.')
# if select_report == str(2):
#     try:
#         shutil.move(arch_path, new_arch)
#     except:
#         print('Could not archive the old rpt_open_CAPRS.csv file.')
# if select_report == str(3):
#     try:
#         shutil.move(arch_path, new_arch)
#     except:
#         print('Could not archive the old test.csv file.')



