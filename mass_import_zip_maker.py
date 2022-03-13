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
    subject_name, dot, file_type = file_name.partition('.')
    return {'file_name': file_name, 'file_size': file_size, 'subject_name': subject_name, 'file_type': file_type}


def method_subject_count():
    user_message(f'\nMax Subjects for this Mass Import: {str(max_subjects)}')

    try:
        subject_count = int(input('How many subjects do you want?: '))
    except ValueError:
        logging.error('Input was not a number, exiting')
        return
    if subject_count <= int(max_subjects):
        return f'Mass Import Subject Count: {str(subject_count)}', subject_count
    else:
        logging.error('You Have Reach Max Count')


def method_zip_size(file_size):
    user_message(f'Max Mass Import Size: {str((MAX_SIZE / 1000000000))} GB')
    try:
        chosen_size = float(input('How large do you want your file to be? (In GB): '))
    except ValueError:
        logging.error('Input was not a number, exiting')
    zip_size_subject_count = chosen_size * 1000000000 / file_size
    if int(zip_size_subject_count) <= int(max_subjects):
        return f'Mass Import Size: {str(chosen_size)}GB', zip_size_subject_count


def duplicate_subject(file_to_duplicate, duplicate_subject_count, directory, relative_directory, archive):
    destination_dir = relative_directory if archive == '1' else directory
    for subject in range(int(duplicate_subject_count)):
        shutil.copy(file_to_duplicate['file_name'],
                    f'{destination_dir}/{file_to_duplicate["subject_name"]}_{subject}.{file_to_duplicate["file_type"]}')
        user_message(
            f'Created {str(subject)} files out of {str(int(duplicate_subject_count))} |'
            f' {str(int((subject / duplicate_subject_count) * 100))}%')


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
    max_subjects = int(MAX_SIZE / file['file_size'])
    method = input('Would you like to: \n(1) Choose Subject Count \nor \n(2) Size in GB\nChoice: ')
    directory_name, subject_count = method_subject_count() if method == '1' else method_zip_size(file['file_size'])
    if not directory_name or not subject_count:
        logging.error('Error, did not get all required data.')
        sys.exit(0)
    archive_type = input('Would you like compress into: \n(1) Zip \nor \n(2) Tar \nChoice: ')
    time.sleep(0.1)
    relative_path, relative_path_inner = create_directory(directory_name, archive_type)
    time.sleep(0.1)
    duplicate_subject(file, subject_count, relative_path, relative_path_inner, archive_type)
    time.sleep(0.1)
    create_archive(relative_path, archive_type)
    time.sleep(0.1)
    user_message('Archive created')
    remove_directory(relative_path)
    user_message('Done! Have a great day.')
