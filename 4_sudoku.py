"""
Sudoku Solver
=============

.. note::

  A description of the sudoku puzzle can be found at:
  `<https://en.wikipedia.org/wiki/Sudoku>`_.

Given a string in ``SDM`` format, described below,
write a program to find and return the solution for the sudoku puzzle
in the string.
The solution should be returned in the same ``SDM`` format as the input.

Some puzzles will not be solvable.
In that case, return the string ``"Unsolvable"``.

The general ``SDM`` format is described here:
`<http://www.sudocue.net/fileformats.php>`_.

For our purposes, each ``SDM`` string will be a sequence of 81 digits,
one for each position on the sudoku puzzle.
Known numbers will be given, and unknown positions will have a zero value.

For example, assume you're given this string of digits:

::

  004006079000000602056092300078061030509000406020540890007410920105000000840600100

The string represents this starting sudoku puzzle:

::

  0 0 4   0 0 6   0 7 9
  0 0 0   0 0 0   6 0 2
  0 5 6   0 9 2   3 0 0

  0 7 8   0 6 1   0 3 0
  5 0 9   0 0 0   4 0 6
  0 2 0   5 4 0   8 9 0

  0 0 7   4 1 0   9 2 0
  1 0 5   0 0 0   0 0 0
  8 4 0   6 0 0   1 0 0

"""

import pathlib
import typing
import time
import itertools

import numpy as np
from sudoku import sudoku

# TODO: pretty print the sudoku
# TODO: create a Sudoku class with read and write and solve methods


def puzzle_from_sdm(
        sdm_file: pathlib.Path
) -> typing.Generator[str, None, None]:
    """
    Read the puzzles from a file in ``.sdm`` format.

    :param sdm_file: file with Sudoku puzzles.
    :type sdm_file: pathlib.Path
    :return: generator holding the string of a puzzle.
    :rtype: typing.Generator[str, None, None]
    """

    with open(sdm_file, mode='r', encoding='utf-8') as f:
        for l, sdm in enumerate(f, 1):
            sdm = sdm.rstrip()
            assert len(sdm) == 81, f'Puzzle at line {l} is not valid'
            yield sdm


def sdm_to_array(sdm_string: str) -> np.ndarray:
    """
    Parse the sdm string to a Numpy ndarray, assuming a 9x9 puzzle.

    :param sdm_string: sdm string with the puzzle.
    :type sdm_string: str
    :return: puzzle converted to Numpy ndarray.
    :rtype: np.ndarray
    """

    sdm = [
        [int(number) for number in sdm_string[row_n - 9:row_n]]
        for row_n in range(9, 90, 9)
    ]
    return np.array(sdm)


def solve_puzzle(sudoku_puzzle: np.ndarray) -> typing.Optional[np.ndarray]:
    """
    Recursive function to solve te Sudoku.

    For each cell, search all the digits which could fit in it.
    When a cell has a unique valid digit,
    update the puzzle with that digit and recall this function.

    If no cell with a single digit is found across the whole Sudoku,
    look for a unique digit among all the valid ones in each row,
    column or region.

    If no other digit is found,
    the puzzle may have multiple solutions and recursion stops.

    :param sudoku_puzzle: puzzle data.
    :type sudoku_puzzle: np.ndarray
    :return: the puzzle updated with new digits until a solution is
        found or ``None`` when multiple solutions are possible.
    :rtype: typing.Optional[np.ndarray]
    """

    # has the puzzle already been solved?
    if 0 not in sudoku_puzzle:
        return sudoku_puzzle

    # list of lists to store the valid digits in each cell
    valid_digits = [
        [
            []
            for row_n in range(9)
        ]
        for col_n in range(9)
    ]

    # cycle over the cells
    for row_n in range(9):
        for col_n in range(9):
            # skip the non-void cells
            if sudoku_puzzle[row_n, col_n] != 0:
                continue

            # define the 3x3 region where the current cell is located
            region = (
                slice(row_n // 3 * 3, (row_n // 3 + 1) * 3),
                slice(col_n // 3 * 3, (col_n // 3 + 1) * 3)
            )

            # check which digit could fit in the current cell
            # -> the digit is not in the row or column or region
            for n in range(1, 10):
                if not(
                        n in sudoku_puzzle[row_n, :] or
                        n in sudoku_puzzle[:, col_n] or
                        n in sudoku_puzzle[region]
                ):
                    valid_digits[row_n][col_n].append(n)

            # does a single digit fit in the current cell?
            # update the puzzle and start the algorithm from scratch
            if len(valid_digits[row_n][col_n]) == 1:
                sudoku_puzzle[row_n, col_n] = valid_digits[row_n][col_n][0]

                return solve_puzzle(sudoku_puzzle)

    # multiple digits fit in each void cell?
    # check all the valid digits looking for a unique valid digit
    # in a row, column or region
    # if it is found, start the algorithm from scratch
    valid_digits_array = np.array(valid_digits, dtype='object')

    # check for single valid digits in rows
    for row_n in range(9):
        digits_to_check = set(
            itertools.chain.from_iterable(
                valid_digits_array[row_n, :].flatten()
            )
        )
        for digit in digits_to_check:
            digit_presence = [
                digit in lst
                for lst in valid_digits_array[row_n, :].flatten()
            ]
            if sum(digit_presence) == 1:
                idx = digit_presence.index(True)
                sudoku_puzzle[row_n, idx] = digit
                return solve_puzzle(sudoku_puzzle)

    # check for single valid digits in columns
    for col_n in range(9):
        digits_to_check = set(
            itertools.chain.from_iterable(
                valid_digits_array[:, col_n].flatten()
            )
        )
        for digit in digits_to_check:
            digit_presence = [
                digit in lst
                for lst in valid_digits_array[:, col_n].flatten()
            ]
            if sum(digit_presence) == 1:
                idx = digit_presence.index(True)
                sudoku_puzzle[idx, col_n] = digit
                return solve_puzzle(sudoku_puzzle)

    # create regions and check for single valid digits among them
    regions = [
        (
            slice(row_n // 3 * 3, (row_n // 3 + 1) * 3),
            slice(col_n // 3 * 3, (col_n // 3 + 1) * 3)
        )
        for row_n in range(0, 9, 3) for col_n in range(0, 9, 3)
    ]
    for region in regions:
        digits_to_check = set(
            itertools.chain.from_iterable(
                valid_digits_array[region].flatten()
            )
        )
        for digit in digits_to_check:
            digit_presence = [
                digit in lst
                for lst in valid_digits_array[region].flatten()
            ]
            if sum(digit_presence) == 1:
                # with regions, the idx is the progressive position
                idx = digit_presence.index(True)
                # convert idx to row and column number
                target_row = idx // 3 + region[0].start
                target_col = idx % 3 + region[1].start
                sudoku_puzzle[target_row, target_col] = digit
                return solve_puzzle(sudoku_puzzle)

    return None


if __name__ == '__main__':
    # read the sdm file
    for i, raw_puzzle in enumerate(
            puzzle_from_sdm(pathlib.Path('./sudoku_puzzles.sdm')), 1
    ):
        # convert string to array
        puzzle = sdm_to_array(raw_puzzle)
        # instantiate the same puzzle with the sudoku library (py-sudoku)
        # to check my result against it
        comparison_puzzle = sudoku.Sudoku(3, 3, board=puzzle.tolist())

        # solve the puzzle timing it
        tic = time.perf_counter()
        solution = solve_puzzle(puzzle)
        toc = time.perf_counter()

        # report the result
        if solution is None:
            print(f'Puzzle {i}: I found no solution, "Unsolvable"')
            print(comparison_puzzle.solve())

            print('=' * 30)
        else:
            # check my result with the comparison one
            assert solution.tolist() == comparison_puzzle.solve().board
            print(
                f'Puzzle {i}: solved in {toc - tic:.4f}s, the solution is',
                solution,
                '=' * 30,
                sep='\n'
            )
