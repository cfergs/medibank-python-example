# pylint: disable=line-too-long
"""
Assumptions: When asking for strings in file will just consider this to be the different words written in the file.

This script will
1. Get a list of files from a directory/ subdirectory
2. For each file grab a list of words
3. Output the list of unique words with more than 2 occurances. Listed in descending order of occurrences.
"""

import argparse
import logging
import os
from collections import Counter

logger = logging.getLogger()
logger.setLevel(logging.INFO)


# Commentary: leveraging type hints where possible
def get_filenames(folder_path: str) -> list[str]:
    """
    Function to obtain a list of filenames from a path.
    This will run recursively against the provided path.

    Will return as a list of strings
    ['./folder/example.txt', './folder/folder1/example.txt', './folder/folder2.file.txt']
    """

    file_name_path = []

    # Get recursive list of files and path from the provided path
    # Commentary: simplest way i could find to do it without running against each subfolder.
    walked_path = os.walk(folder_path)

    # Next take the file names for each path and then output items to a list.
    for directory, _, files in walked_path:
        for file in files:
            file_name_path.append(os.path.join(directory, file))

    return file_name_path


def get_file_string_values(filenames: list) -> list[str]:
    """
    Function to go into a file and grab a list of words

    Will return as a list of strings:
    ['word', 'word', 'word', word']
    """

    string_values = []

    # Commentary: probably better if filtered to certain filetypes
    for file in filenames:
        with open(file, "r", encoding="utf-8") as file:
            content = file.read()
        string_values.append(content.lower().split())

    # Flatten as previous step has created lists of lists and we need just a list
    string_values = [word for sublist in string_values for word in sublist]
    return string_values


def count_unique_words(string_values: list[str]) -> dict:
    """
    Function to count each occurence of a word.
    This function will only return a dictionary of words that occur more than 2 times.

    Will return as a dictionary:
    {'top': 2, 'secret': 2, 'file': 10, 'with': 10, 'stuff': 2, 'in': 10, 'it': 10, 'text': 8}
    """

    # Commentary: discovered counter while writing this script. Very impressive and just outputs as a dictionary

    # Get a count of unique filenames
    unique_count = Counter(string_values)

    # Filter out words occuring less than twice
    # Commentary: filtering out before returning is my preferred method of doing this
    filtered_counter = {key: count for key, count in unique_count.items() if count >= 2}

    logger.debug("Filtered Counter output is %s", filtered_counter)

    return filtered_counter


def main():
    """
    Main Function. Invokes other sub-functions
    """

    # Commentary: pull in argument for filepath. Errors if path not specified
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str, help="Specify path to find unique strings")

    args = parser.parse_args()

    # Commentary: wrapped in a try to catch errors if they occur
    try:
        # Getting to the meat and potatoes of the script
        filenames = get_filenames(args.path)
        file_strings = get_file_string_values(filenames)
        string_count = count_unique_words(file_strings)

        # Final step if string_count contains any results
        if string_count:
            for key, value in sorted(string_count.items(), key=lambda x: x[1], reverse=True):

                # Commentary: Naughty alert - used chatgpt for this line as I couldn't think of a efficient way to do this.
                # Basically am sorting results based on highest to lowest value so i can then print them.
                # Really interesting way of doing it, you learn something new everyday!
                # Potentially another way could be to find max value, print, remove then recheck continually. Just not as nice

                print(f"{key} {value}")

    # Commentary: delibrately broad as unsure what would occur.
    # In real usage would be more aligned to specific type errors
    except Exception as error:  # pylint: disable=broad-exception-caught
        logger.error("Something Bad happened")
        logger.error(error)


if __name__ == "__main__":
    main()
