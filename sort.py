from pathlib import Path
import sys
from shutil import move
import logging
from threading import Thread, Condition

def replace_file(file: Path, condition: Condition):
    with condition:
        condition.wait()

    base_folder = file.parent
    cat_folder = base_folder / file.suffix.lstrip('.')
    cat_folder.mkdir(exist_ok=True)
    move(file, cat_folder)

def form_files(folder: Path, prev_condition: Condition):
    with prev_condition:
        prev_condition.wait()
    file_remove_threads = []
    folder_threads = []
    new_condition = Condition()
    for item in folder.iterdir():
        if item.is_file():
            replace_thread = Thread(target=replace_file, args=(item, new_condition))
            file_remove_threads.append(replace_thread)
            replace_thread.start()
        else:
            folder_thread = Thread(target=form_files, args=(item, new_condition))
            folder_threads.append(folder_thread)
            folder_thread.start()
    with new_condition:
        new_condition.notify_all()
    [th.join() for th in folder_threads]
    [th.join() for th in file_remove_threads]

def main(folder: Path):
    first_condition = Condition()
    main_folder_thread = Thread(target=form_files, args=(folder, first_condition))
    main_folder_thread.start()
    with first_condition:
        first_condition.notify_all()
    main_folder_thread.join()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
    try:
        path = sys.argv[1]
    except IndexError:
        path = input('You didn\'t write path. Please write path here: ')
    folder = Path(path)

    while True:
        if folder.is_dir():
            break
        else:
            path = input('There are no folders on this path. Please write another: ')
            folder = Path(path)

    main(folder)
    pass





