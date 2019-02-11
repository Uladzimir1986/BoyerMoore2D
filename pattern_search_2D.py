# Copyright 2019 Vladimir Vilchinsky.
"""
    This module searches a text file for two-dimensional pattern and prints number of pattern occurrences.
"""

from argparse import ArgumentParser
import collections
import os.path
import sys

DGRAM_MAX_D_VALUE = 3

class PatternSearch2D(): # pylint: disable=too-few-public-methods, too-many-instance-attributes
    """PatternSearch2D counts number of occurrences of the specific two-dimensional pattern in a text.

    The algorithm is implementation of the idea from paper:
    "A Boyer-Moore Approach for Two-Dimensional Matching"
    https://pdfs.semanticscholar.org/ec0b/8b247b9a6efdbe8b3ddc2e4e3547cecf5223.pdf.
    This implementation is modified for arbitrary shapes of pattern and text.
    Average case complexity is sub-linear. Worst time complexity is O(m^2n^2).
    ...
    Attributes:
    ----------
    pattern : str
        Pattern string

    Methods:
    ----------
    count_matches(text)
        Counts and returns number of occurrences of the two-dimensional pattern in the text

    Raises:
    ----------
        ValueError: If pattern is empty string.
    """

    def __init__(self, pattern):
        if not pattern:
            raise ValueError('pattern can not be empty string')
        self.pattern = pattern
        self.__trivial_checks = None
        self.__pattern_matrix = PatternSearch2D.__text_to_matrix(self.pattern)

        self.__pattern_min_row_length = min([len(row) for row in self.__pattern_matrix])

        'd-gram is a kind of a fingerprint of the pattern'
        self.__d_value = max(min(DGRAM_MAX_D_VALUE, self.__pattern_min_row_length - 1), 1)
        self.__dgram_vertical_skip = collections.defaultdict(lambda: len(self.__pattern_matrix))

        self.__dgram_hor_pos = collections.defaultdict(lambda: -1)
        self.__dgram_hor_pos_linked_list = [0] * self.__pattern_min_row_length
        self.__strip_length = self.__pattern_min_row_length - self.__d_value + 1

        for i in range(0, len(self.__pattern_matrix)):
            for j in range(0, self.__strip_length):
                dgram_value = self.__pattern_matrix[i][j:j+self.__d_value]

                if i == len(self.__pattern_matrix) - 1:
                    self.__dgram_hor_pos_linked_list[j] = self.__dgram_hor_pos[dgram_value]
                    self.__dgram_hor_pos[dgram_value] = j
                elif self.__dgram_vertical_skip[dgram_value] > len(self.__pattern_matrix) - i - 1:
                    self.__dgram_vertical_skip[dgram_value] = len(self.__pattern_matrix) - i - 1

    def count_matches(self, text):
        """Counts and returns number of occurrences of the pattern in the text

        Parameters:
        ----------
        text : str

        Returns:
        ----------
        int
            number of occurrences of pattern in the text
        """

        if not text:
            return 0

        self.__trivial_checks = 0
        self.__text = PatternSearch2D.__text_to_matrix(text)
        max_number_of_columns = max([len(row) for row in self.__text])
        j = self.__strip_length - 1
        count = 0
        while j < max_number_of_columns - self.__pattern_min_row_length + self.__strip_length:
            i = len(self.__pattern_matrix) - 1

            while i < len(self.__text):
                dgram_value = self.__text[i][j:j + self.__d_value]
                k = self.__dgram_hor_pos[dgram_value]

                while k > -1:
                    count += self.__trivial_check_position(i - len(self.__pattern_matrix) + 1, j - k)
                    k = self.__dgram_hor_pos_linked_list[k]

                i = i + self.__dgram_vertical_skip[dgram_value]

            j = j + self.__strip_length

        return count

    def __trivial_check_position(self, i, j):
        """Performs trivial iteration check if the pattern starts on position i, j in the text

        The algorithm minimizes number of calls to this method

        Parameters:
        ----------
        i : int
        j : int

        Returns:
        ----------
        bool
            True if pattern top left corner starts on position i, j. False otherwise.
        """

        self.__trivial_checks += 1
        if i < 0 or i >= len(self.__text):
            return False
        if j < 0 or j >= len(self.__text[i]):
            return False

        for pattern_i in range(0, len(self.__pattern_matrix)):
            for pattern_j in range(0, len(self.__pattern_matrix[pattern_i])):
                if (i + pattern_i >= len(self.__text) or j + pattern_j >= len(self.__text[i + pattern_i])
                        or self.__text[i + pattern_i][j + pattern_j] != self.__pattern_matrix[pattern_i][pattern_j]):
                    return False

        return True

    @staticmethod
    def __text_to_matrix(text):
        """Converts text to array of strings, filtering out empty lines from result array

        Parameters:
        ----------
        text : str

        Returns:
        ----------
        [str]
        """
        matrix = text.replace('\r', '').split('\n') #filter out \r for Windows environment files
        matrix = [x for x in matrix if x]

        return matrix

def read_file(file_path):
    """Reads file content and returns it as a string.
    If file does not exist or error occurs on read, error message is shown and program exists

    Parameters:
    ----------
    file_path : string
        path to the file

    Returns:
    ----------
    str
        File content.
    """
    if not os.path.exists(file_path):
        print("File not found %s." % file_path)
        sys.exit(1)

    try:
        return open(file_path, 'r').read()
    except IOError:
        print("Error reading file %s." % file_path)
        sys.exit(1)

def main():
    """ Main method parses arguments, executes PatternSearch and prints patterns count
    """

    parser = ArgumentParser(description="Pattern search")
    parser.add_argument("-p", "--patternFile", required=True,
                        help="File with pattern definition")
    parser.add_argument("-t", "--textFile", required=True,
                        help="File with text")
    args = parser.parse_args()

    pattern = read_file(args.patternFile)
    text = read_file(args.textFile)
    pattern_search = PatternSearch2D(pattern)
    print(pattern_search.count_matches(text))

if __name__ == '__main__':
    main()
