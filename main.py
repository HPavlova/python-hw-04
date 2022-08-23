import argparse
import concurrent.futures
from pathlib import Path
from shutil import copyfile
import logging

parser = argparse.ArgumentParser(description='Sorting folder')
parser.add_argument('-s', '--source', help='source folder')
parser.add_argument('-o', '--output', default='dist', help='output folder')
args = vars(parser.parse_args())
source = args.get('source')
output = args.get('output')
output_folder = Path(output)


def reader(path: Path) -> list:
    result = []
    for item in path.iterdir():
        if item.is_dir():
            print(f"{item} - is folder")
            if len(reader(item)):
                result = result + reader(item)
        else:
            print(f"{item} - is file")
            result.append(item)
    return result


def copy_file(file: Path) -> None:
    ext = file.suffix
    new_path = output_folder/ext
    new_path.mkdir(parents=True, exist_ok=True)
    copyfile(file, new_path / file.name)
    logging.info(f'{file.name} copied')


if __name__ == '__main__':
    path = input("Enter path to folder: ").strip()
    source_path = Path(path).resolve()

    if len(path) < 1:
        print("Path is empty.Try again!")
    if not Path(path).exists():
        print("Path is not exists.Try again!")
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            futures = []
            for el in reader(source_path):
                futures.append(executor.submit(copy_file, el))
        logging.info('Done')
