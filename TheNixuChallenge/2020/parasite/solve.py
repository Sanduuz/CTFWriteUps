#!/usr/bin/env python3

import os
from PIL import Image
from typing import Generator


def read_lines(file_path: str) -> Generator[str, None, None]:
    """Read lines from file using a generator instead of reading the whole file to memory"""
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            yield line.strip()


def normalize_analog_value(value: float) -> int:
    """Normalize float value and return the pixel color as int for grayscale image"""
    value += 0.137  # Minimum value for analog signal was -0.137 so scale everything up by that amount.
    return int(value * 255)  # Convert float to int, rounding to nearest integer simultaneously.


def check_hsync(time_elapsed: int, field2: int, field3: int) -> bool:
    """Check if hsync is occuring"""
    # Note: if vsync is occuring (field3 == 0), ignore hsync signal
    return field2 == 0 and field3 != 0 and time_elapsed > 30 * 10**3  # 30 microseconds


def check_vsync(time_elapsed: int, field2: int, field3: int) -> bool:
    """Check if vsync is occuring"""
    return field3 == 0 and time_elapsed > 16.5 * 10**6  # 16.5 milliseconds


def main():
    column = 0
    row = 0

    last_hsync = 0
    last_vsync = 0
    frames = 0

    image = Image.new("L", (398, 525), "white")  # Create new grayscale image
    pixels = image.load()

    print("Parsing frames...")
    if not os.path.isdir("frames"):
        print("'frames' directory does not exist. Creating...")
        os.mkdir("frames")

    for line in read_lines("data"):
        timestamp, field2, field3, analog = line.split(",")
        
        if analog == '':
            # Handle timestamp
            seconds, nanoseconds = map(int, timestamp.split("."))
            
            # Convert seconds to nanoseconds
            nanoseconds += seconds * 10**9

            # Check for vsync (check this first since it's more rare)
            if check_vsync(nanoseconds - last_vsync, int(field2), int(field3)):
                column = 0
                row = 0
                last_vsync = nanoseconds

                # Save the frame and start a new frame
                image.save(f"frames/frame_{frames:0>3}.png")
                frames += 1
                image = Image.new("L", (398, 525), "white")
                pixels = image.load()
                continue

            # Check for hsync
            if check_hsync(nanoseconds - last_hsync, int(field2), int(field3)):
                # if hsync in progress, column = 0, row += 1
                column = 0
                row += 1
                last_hsync = nanoseconds
                continue

            continue

        # Write pixel
        try:
            pixels[column, row] = normalize_analog_value(float(analog))
        except IndexError:
            # Some overflow on first line but we can ignore this.
            # print(f"Overflowing image dimensions! {column=} {row=}")
            pass

        column += 1


if __name__ == "__main__":
    main()
