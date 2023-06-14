#!/usr/bin/env python3

import io
import os
import argparse
import datetime
import traceback

from typing import Union


def verify_magic_bytes(header: bytes) -> bool:
    """
    Verify that file starts with NXA magic bytes.

    :param header: First 3 bytes of the file.

    :returns: If file is valid NXA archive
    """

    if header == b"NXA":
        return True
    else:
        return False


def read_archive(filename: str) -> Union[io.BufferedReader, bool]:
    """
    Read archive and return its contents.

    :param filename: Filename of the archive.

    :returns: File handle if valid NXA archive, otherwise bool.
    """

    if os.path.isfile(filename):
        file_handle = open(filename, "rb")
        file_header = file_handle.read(3)
        if verify_magic_bytes(file_header):
            return file_handle
        else:
            print("Not a valid NXA archive.")
            return False
    else:
        print(f"File {filename} does not exist!")
        return False


def read_bytes(length: bytes, file_handle: io.BufferedReader) -> bytes:
    """
    Read bytes of length and return bytes.

    :param length: Number of bytes to read.
    :param file_handle: Open file handle (BufferedReader) to read from.

    :returns: bytes up to *length*.
    """

    number_of_bytes_to_read = int.from_bytes(length, byteorder="little")
    return file_handle.read(number_of_bytes_to_read)


def write_file(filename: str, file_contents: bytes) -> None:
    """
    Write a file.

    :params filename: The name to save the file as.
    :params file_contents: The bytes that will be saved.
    """

    print(f"Writing file: {filename}")

    with open(filename, "wb") as f:
        f.write(file_contents)


def read_file(filename: str) -> bytes:
    """
    Read a file.

    :params filename: Name of the file to be read.

    :returns: The file contents in bytes.
    """

    with open(filename, "rb") as f:
        return f.read()


def unpack_archive(archive_name: str, output_directory: str, overwrite_all: bool) -> None:
    """
    Unpack given NXA archive based on lengths parsed from file.

    :param archive_name: Filename of archive.
    :param output_directory: string name of output directory.
    :param overwrite_all: If true, clear directory contents before unpacking new archive.
    """

    files_not_extracted = True

    if overwrite_all:
        for file in os.listdir(output_directory):
            os.remove(f"{output_directory}/{file}")

    archive_fh = read_archive(archive_name)

    while files_not_extracted:
        try:
            filename_size = archive_fh.read(4)  # Read 4 bytes that contain the length of the filename inside the archive.
            filename = read_bytes(filename_size, archive_fh)  # Read bytes up to size from previous step.

            if len(filename) == 0:  # We have reached the end of archive.
                files_not_extracted = False
            else:
                file_contents_size = archive_fh.read(4)
                file_contents = read_bytes(file_contents_size, archive_fh)

                # Save file
                write_file(f"{output_directory}/{filename.decode()}", file_contents)
        except Exception as err:
            stack_trace = traceback.format_exc()
            print(f"Caught an exception! Debug information:\n\n{stack_trace}")

    archive_fh.close()

    print(f"Archive '{archive_name}' unpacked successfully.")


def pack_archive(archive_name: str, input_directory: str) -> None:
    """
    Pack files from input_directory to filename archive.

    :param archive_name: Filename of archive to be saved.
    :param input_directory: string name of input directory.
    """

    archive_fh = open(archive_name, "wb")
    archive_fh.write(b"NXA")  # Write the correct header.

    for file in os.listdir(input_directory):
        try:
            filename_size = len(file.encode())
            archive_fh.write(int.to_bytes(filename_size, length=4, byteorder="little"))  # Write the length of the filename into the archive.
            archive_fh.write(file.encode())  # Write filename

            file_contents = read_file(f"{input_directory}/{file}")
            file_contents_size = len(file_contents)
            archive_fh.write(int.to_bytes(file_contents_size, length=4, byteorder="little"))  # Write the length of the file contents into the archive.
            archive_fh.write(file_contents)
        except Exception as err:
            stack_trace = traceback.format_exc()
            print(f"Caught an exception! Debug information:\n\n{stack_trace}")
    
    archive_fh.close()

    print(f"Saved archive as '{archive_name}'.")


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()  # We don't want to pack and unpack at the same time.

    parser.add_argument(
        "-f",
        "--file",
        help="NXA archive to unpack/pack.",
        type=str,
        required=True
    )

    group.add_argument(
        "-o",
        "--output",
        help="Output directory for unpacking NXA archives.",
        type=str
    )

    group.add_argument(
        "-i",
        "--input",
        help="Input directory for packing NXA archives.",
        type=str
    )

    parser.add_argument(
        "--overwrite-all",
        help="Clear output directory before unpacking new archive.",
        action="store_true"
    )

    args = parser.parse_args()

    # If -o or -i arguments are not given, default to -o with default value of datetime_OUTPUT
    if not args.input and not args.output:
        args.output = f"{datetime.datetime.now().strftime('%d_%m_%Y_-_%H_%M_%S_{0}_OUTPUT'.format(args.file))}"

    if args.output:
        if os.path.isfile(args.file):
            # Create directory if it does not exist.
            if not os.path.isdir(args.output):
                print(f"Directory {args.output} does not exist. Creating...")
                os.makedirs(args.output)

            unpack_archive(args.file, args.output, args.overwrite_all)
        else:
            print(f"Archive '{args.file}' does not exist! Exiting...")
    else:
        # Verify that input directory exists.
        if os.path.isdir(args.input):
            pack_archive(args.file, args.input)
        else:
            print(f"Directory '{args.input}' does not exist! Exiting...")


if __name__ == "__main__":
    main()
