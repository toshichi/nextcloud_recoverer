import os
import shutil


def get_files(input_dir):
    files_list = []
    for _fpath, _, _files in os.walk(input_dir):
        # for all files in folder
        for _file in _files:
            files_list.append(
                os.path.join(_fpath, _file))
    return files_list

# check first line of this file
def file_checker(file, key):
    try:
        with open(file, 'rb') as f:
            # read first 10 lines
            for _ in range(10):
                if key.encode() in f.readline():
                    return True
    except OSError as e:
        print("\r\033[KOSError: {}".format(e))
        return False
    return False

# if file size same, recover copy from backup
def file_recover(file, backup_path_prefix, check_path_prefix):
    path_main = file[len(check_path_prefix):].strip('\\')
    backup_file = os.path.join(backup_path_prefix, path_main)
    if os.path.exists(backup_file):
        if os.path.getsize(file) == os.path.getsize(backup_file):
            print("\r\033[KRecovering {}".format(file), end="")
            os.remove(file)
            shutil.copy(backup_file, file)
            return True
        else:
            print("\r\033[KFile size not same, not recover {}".format(file), end="")
            return False
    else:
        print("\r\033[KBackup file not exist, not recover {}".format(file), end="")
        return False


if __name__ == '__main__':
    backup_path = '\\\\192.168.31.11\\b1\\CloudData\\tojo\\files\\Shokaku\\LiveBackup\\Documents'
    check_path = 'D:\\Home\\Documents'
    print('Get files from input directory...', end="")
    files = get_files(check_path)
    print('{} files got'.format(len(files)))
    print('Check files')
    counter = 0
    found_files = []
    for _file in files:
        # print progress
        counter += 1
        print(f'\r\033[K{counter}/{len(files)} {_file[:25]}...{_file[-25:]}', end='')
        if file_checker(_file, 'coder17.com | 522: Connection timed out'):
            print(f'\r\033[K**Found: {_file}')
            found_files.append(_file)
    print('\r\033[KDone')
    print(f'Found {len(found_files)} files')
    print('Recover files')
    recovered_files = []
    unrecovered_files = []
    for _found in found_files:
        # print(f'\r\033[KRecover: {_found}', end='')
        if file_recover(_found, backup_path, check_path):
            recovered_files.append(_found)
        else:
            unrecovered_files.append(_found)
    print('\r\033[KDone')
    print(f'Recovered {len(recovered_files)} files')
    print(f'Unrecovered {len(unrecovered_files)} files')


