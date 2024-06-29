from typing import List, Optional

import h5py
import numpy as np
from tqdm import tqdm


def print_header(text: str) -> None:
    print("=" * 40)
    print(text)
    print("=" * 40)


def structure_printer(file, shape: bool = True, indent=0):
    space = 32 - 2 * indent - 2
    if isinstance(file, h5py.Dataset):
        if shape:
            print(f" :: {str(file.dtype):8} : {file.shape}", end="")

        return

    for key in file:
        print("\n|-" + indent * "--" + key.ljust(space), end="")
        structure_printer(file[key], shape, indent + 1)


def write(
    input_file, output_file, path: Optional[List[str]] = None, verbose: bool = True
):
    if path is None:
        path = []

    for key, value in input_file.items():
        current_subpath = path + [key]
        if isinstance(value, np.ndarray):
            if verbose:
                print(f"Creating {'/'.join(current_subpath)}: Shape {value.shape}")
            output_file.create_dataset("/".join(current_subpath), data=value)
        else:
            write(input_file[key], output_file, current_subpath, verbose=verbose)


def load_dataset(dataset):
    values = dataset[:]
    if values.dtype == np.float64:
        values = values.astype(np.float32)

    if values.dtype == np.int32:
        values = values.astype(np.int64)

    return values


def read(file, level: int = 0, path=None):
    if path is None:
        path = []
    if isinstance(file, h5py.Dataset):
        return load_dataset(file)

    iterator = file
    if level == 1:
        iterator = tqdm(file, f"Loading {path[-1]}")

    return {key: read(file[key], level + 1, path + [key]) for key in iterator}


def extract(file):
    if isinstance(file, h5py.Dataset):
        return file[:]

    return {key: extract(file[key]) for key in file}


def concatenate(head, *tail, path: Optional[List[str]] = None):
    if path is None:
        path = []

    if not isinstance(head, dict):
        return np.concatenate((head, *tail))

    database = {}
    for key in head:
        new_path = path + [key]
        print(f"Concatenating: {'/'.join(new_path)}")
        try:
            database[key] = concatenate(
                head[key], *[d[key] for d in tail], path=new_path
            )
        except KeyError:
            print(f"Skipping: {'/'.join(new_path)}")
            continue

    return database
