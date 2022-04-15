import logging
import os
import shutil
import sys
import time

# region Defaults
MAX_SIZE = 15000000000

logging.basicConfig(level=os.getenv('LOG_LEVEL', logging.INFO),
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M')


# endregion


def user_message(string):
    logging.info(string)


def receive_file():
    file_name = input("What's the file's name?: ")
    file_size = os.path.getsize(file_name)
    file_name, dot, file_type = file_name.partition('.')
    return {'file_name': file_name, 'file_size': file_size, 'file_type': file_type}


def method_file_count():
    user_message(f'\nMax files for this zip: {str(max_files)}')

    try:
        file_count = int(input('How many images do you want?: '))
    except ValueError:
        logging.error('Input was not a number, exiting')
        return
    if file_count <= int(max_files):
        return f'Archive file count: {str(file_count)}', file_count
    else:
        logging.error('Max files count reached')


def method_zip_size(file_size):
    user_message(f'Zip Size: {str((MAX_SIZE / 1000000000))} GB')
    try:
        chosen_size = float(input('How large do you want your archive to be? (In GB): '))
    except ValueError:
        logging.error('Input was not a number, exiting')
    zip_size_file_count = chosen_size * 1000000000 / file_size
    if int(zip_size_file_count) <= int(max_files):
        return f'Archive size: {str(chosen_size)}GB', zip_size_file_count


def duplicate_file(file_to_duplicate, duplicate_file_count, directory, relative_directory, archive):
    destination_dir = relative_directory if archive == '1' else directory
    for file in range(int(duplicate_file_count)):
        shutil.copy(file_to_duplicate['file_name'],
                    f'{destination_dir}/{file_to_duplicate["file_name"]}_{file}.{file_to_duplicate["file_type"]}')
        user_message(
            f'Created {str(file)} files out of {str(int(duplicate_file_count))} |'
            f' {str(int((file / duplicate_file_count) * 100))}%')


def create_directory(directory, archive):
    if os.path.exists("output") == 0:
        os.mkdir('output')
    path = f'output/{directory}'
    os.mkdir(path)
    if archive == '1':
        path_inner = f'{path}/{directory}_inner'
        os.mkdir(path_inner)
        return path, path_inner
    else:
        return path, path


def remove_directory(directory):
    remove = input('Remove directory? (does not remove Archive file) Y/N: ')
    if remove.lower() == 'y':
        shutil.rmtree(directory)
        user_message('Directory was deleted (this might take a few seconds to take effect)')
    else:
        user_message('Directory will not be deleted')


def create_archive(relative_directory_path, archive):
    if archive == '1':
        user_message('Compressing file to ZIP, please wait :)')
        shutil.make_archive(relative_directory_path, 'zip', relative_directory_path)  # TODO: Add progress
    else:
        user_message('Compressing file to TAR, please wait :)')
        shutil.make_archive(relative_directory_path, 'tar', relative_directory_path)  # TODO: Add progress
    user_message('Archive created')


if __name__ == '__main__':
    file = receive_file()
    max_files = int(MAX_SIZE / file['file_size'])
    method = input('Would you like to: \n(1) Choose File Count \nor \n(2) Size in GB\nChoice: ')
    directory_name, file_count = method_file_count() if method == '1' else method_zip_size(file['file_size'])
    if not directory_name or not file_count:
        logging.error('Error, did not get all required data.')
        sys.exit(0)
    archive_type = input('Would you like compress into: \n(1) Zip \nor \n(2) Tar \nChoice: ')
    time.sleep(0.1)
    relative_path, relative_path_inner = create_directory(directory_name, archive_type)
    time.sleep(0.1)
    duplicate_file(file, file_count, relative_path, relative_path_inner, archive_type)
    time.sleep(0.1)
    create_archive(relative_path, archive_type)
    time.sleep(0.1)
    user_message('Archive created')
    remove_directory(relative_path)
    user_message('Done! Have a great day.')
