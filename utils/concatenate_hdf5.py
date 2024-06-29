from argparse import ArgumentParser
from glob import glob

from h5py import File
from shared import concatenate, extract, print_header, write


def main(input_folder: str, output_file: str) -> None:
    combine_header("Reading in files from ", input_folder)
    global_file = []
    for filename in glob(f"{input_folder}/*.h5"):
        print(f"Reading: {filename}")
        with File(filename, "r") as file:
            global_file.append(extract(file))

    print("=" * 40)

    print()
    print_header("Concatenating Files")

    global_file = concatenate(*global_file)
    print("=" * 40)
    print()

    combine_header("Writing Output to ", output_file)
    with File(output_file, "w") as output_file:
        write(global_file, output_file)
    print("=" * 40)


def combine_header(text: str, path: str) -> None:
    print_header(text + path)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "input_folder",
        type=str,
        help="Folder of HDF5 files to concatenate.",
    )
    parser.add_argument(
        "output_file",
        type=str,
        help="Complete HDF5 file to create for output.",
    )

    args = parser.parse_args()
    main(args.input_folder, args.output_file)
