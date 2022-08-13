import shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from normalize import normalize
from time import sleep
from random import random


def folder_parse(source_folder: Path, output_folder: Path) -> None:
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for future in futures:
            print(future.result())

        for item in source_folder.iterdir():
            if item.is_dir():
                futures.append(executor.submit(folder_parse, item, output_folder))
            else:
                futures.append(executor.submit(copy_file, item, output_folder))

    if output_folder != source_folder:
        handle_delete_folder(source_folder)


def copy_file(file: Path, output_folder: Path) -> None:
    file_folder = file.suffix[1:].upper()
    if file.suffix in ('.jpeg', '.jpg', '.png', '.svg'):
        return handle_media(file, output_folder / 'Images' / file_folder)
    if file.suffix in ('.mp3', '.ogg', '.wav', '.amr'):
        return handle_media(file, output_folder / 'Audio' / file_folder)
    if file.suffix in ('.mp4', '.avi', '.mkv', '.mov'):
        return handle_media(file, output_folder / 'Video' / file_folder)
    if file.suffix in ('.pdf', '.doc', '.docx', '.xlsx', '.txt', '.pptx', '.xml'):
        return handle_documents(file, output_folder / 'Documents' / file_folder)
    if file.suffix in ('.zip', '.tar', '.gz'):
        return handle_archive(file, output_folder / 'Archives')
    else:
        return handle_other(file, output_folder / 'Trash')


def handle_media(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))


def handle_documents(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))


def handle_other(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))


def handle_archive(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    folder_for_file = target_folder / normalize(filename.name.replace(filename.suffix, ''))
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(str(filename.resolve()), str(folder_for_file.resolve()))
    except shutil.ReadError:
        print(f'Обман - это не архив {filename}!')
        folder_for_file.rmdir()
        return None
    filename.unlink()


def handle_delete_folder(folder: Path):
    if folder.is_dir():
        try:
            folder.rmdir()
        except OSError:
            print(f'Folder {folder} was not deleted!')
    else:
        print(f'{folder} is not a folder!')