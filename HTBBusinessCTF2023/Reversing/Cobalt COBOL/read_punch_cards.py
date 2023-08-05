#!/usr/bin/env python3

#                                         MASTERCARD
#     __________________________________________________________________________________
#    / &-0123456789ABCDEFGHIJKLMNOPQR/STUVWXYZ:#@'=".{(+|!$*);,%_}?                     \
# 12|  x           xxxxxxxxx                        xxxxx                                |
# 11|   x                   xxxxxxxxx                    xxxxx                           |
#  0|    x                           xxxxxxxxx                xxxxx                      |
#  1|     x        x        x        x                                                   |
#  2|      x        x        x        x       x          x                               |
#  3|       x        x        x        x       x    x     x   x                          |
#  4|        x        x        x        x       x    x     x   x                         |
#  5|         x        x        x        x       x    x     x   x                        |
#  6|          x        x        x        x       x    x     x   x                       |
#  7|           x        x        x        x       x    x         x                      |
#  8|            x        x        x        x xxxxxxxxxxxxxxxxxxxxx                      |
#  9|             x        x        x        x                                           |
#   |____________________________________________________________________________________| 
# 

def read_cards(punch_card_file: str) -> list[list[list[str]]]:
    """
    Read punch cards from text file and return them.

    :param punch_card_file: Name of text file containing the punch cards in ascii art.

    :returns: List of each row with columns as string (either "" or "x") in a list.
                For example the following (small) card:
                   ____________
                  /            \
                1|    x         |
                2|  x           |
                3|   x          |
                 |______________|
                Would return:
                [[[" ", " ", "x"], ["x", " ", " "], [" ", "x", " "]]]
    """
    cards = []

    with open(punch_card_file) as file:
        cards_data = file.read().split("\n\n")

    for card_data in cards_data:
        card = []
        for row in card_data.split("\n"):
            # Only look at lines starting with digits
            if row.strip() != "" and row.strip()[0].isdigit():
                # Read only between positions 6 to 80 (74 columns)
                card.append(list(row[5:79]))
        cards.append(card)

    return cards


def translate_punch_cards(hole_positions: dict) -> str:
    """
    Translate punch cards to ASCII text.

    :param hole_positions: Dict containing hole positions from `read_hole_positions` function.

    :returns: ASCII text translation of punch cards.
    """

    translated_ascii = ""

    # "<SYMBOL>": [<ROWS>]
    translation_table = {
        "&": [12], "-": [11], "0": [0], "1": [1], "2": [2], "3": [3], "4": [4], "5": [5], "6": [6], "7": [7], "8": [8], "9": [9],
        "A": [12, 1], "B": [12, 2], "C": [12, 3], "D": [12, 4], "E": [12, 5], "F": [12, 6], "G": [12, 7], "H": [12, 8], "I": [12, 9],
        "J": [11, 1], "K": [11, 2], "L": [11, 3], "M": [11, 4], "N": [11, 5], "O": [11, 6], "P": [11, 7], "Q": [11, 8], "R": [11, 9],
        "/": [0, 1], "S": [0, 2], "T": [0, 3], "U": [0, 4], "V": [0, 5], "W": [0, 6], "X": [0, 7], "Y": [0, 8], "Z": [0, 9],
        ":": [2, 8], "#": [3, 8], "@": [4, 8], "'": [5, 8], "=": [6, 8], "\"": [7, 8],
        ".": [12, 3, 8], "{": [12, 4, 8], "(": [12, 5, 8], "+": [12, 6, 8], "|": [12, 7, 8],
        "!": [11, 2, 8], "$": [11, 3, 8], "*": [11, 4, 8], ")": [11, 5, 8], ";": [11, 6, 8],
        ",": [0, 3, 8], "%": [0, 4, 8], "_": [0, 5, 8], "}": [0, 6, 8], "?": [0, 7, 8]
    }

    column_translation_dict = {
        "0": [], "1": [], "2": [], "3": [], "4": [], "5": [], "6": [], "7": [], "8": [], "9": [], "10": [],
        "11": [], "12": [], "13": [], "14": [], "15": [], "16": [], "17": [], "18": [], "19": [], "20": [],
        "21": [], "22": [], "23": [], "24": [], "25": [], "26": [], "27": [], "28": [], "29": [], "30": [],
        "31": [], "32": [], "33": [], "34": [], "35": [], "36": [], "37": [], "38": [], "39": [], "40": [],
        "41": [], "42": [], "43": [], "44": [], "45": [], "46": [], "47": [], "48": [], "49": [], "50": [],
        "51": [], "52": [], "53": [], "54": [], "55": [], "56": [], "57": [], "58": [], "59": [], "60": [],
        "61": [], "62": [], "63": [], "64": [], "65": [], "66": [], "67": [], "68": [], "69": [], "70": [],
        "71": [], "72": [], "73": [], "74": [], "75": [], "76": [], "77": [], "78": [], "79": [], "80": []
    }

    # Loop through holes
    for row in hole_positions.values():
        for column in row:
            # For each column in list, append row number to column_translation_dict. 
            column_translation_dict[str(column)].append(
                int(list(hole_positions.keys())[list(hole_positions.values()).index(row)])
            )

    for character in column_translation_dict.values():
        if len(character) != 0:
            ascii_character = list(translation_table.keys())[list(translation_table.values()).index(character)]
            translated_ascii += ascii_character
        else:
            translated_ascii += " "
        
    return translated_ascii


def read_hole_positions(card: list[list[str]]) -> dict[str, list]:
    """
    Read hole positions from punch card.

    :param cards: Punch cards from `read_cards` function.

    :returns: Dictionary containing the hole columns for given row.
                Format:
                {
                    "<ROW NUMBER>": [<HOLE COLUMN>, <HOLE COLUMN>]
                }

                For example row 12 in the master card would look as follows:
                {
                    "12": [0, 12, 13, 14, 15, 16, 17, 18, 19, 20, 45, 46, 47, 48, 49]
                }
    """

    hole_translation_dict = {
        "12": [],
        "11": [],
        "0": [],
        "1": [],
        "2": [],
        "3": [],
        "4": [],
        "5": [],
        "6": [],
        "7": [],
        "8": [],
        "9": []
    }

    # Read rows 12 and 11
    for row_index, row in enumerate(card[:2]):
        for column_index, column in enumerate(row):
            if column == "x":
                hole_translation_dict[str(12 - row_index)].append(column_index)

    # Read rows 0-9
    for row_index, row in enumerate(card[2:]):
        for column_index, column in enumerate(row):
            if column == "x":
                hole_translation_dict[str(row_index)].append(column_index)

    return hole_translation_dict


def main():
    cards = read_cards("scans.txt")
    
    for card in cards:
        hole_positions = read_hole_positions(card)
        ascii_translation = translate_punch_cards(hole_positions)
        print(ascii_translation)


if __name__ == "__main__":
    main()
