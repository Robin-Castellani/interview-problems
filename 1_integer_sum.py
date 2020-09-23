"""
Sum of Integers Up To n

Write a function, ``add_it_up()``, that takes a single positive
integer as input and returns the sum of the integers from zero
to the input parameter included.

The function should return 0 if a non-integer is passed in.
"""


def add_it_up(integer: int) -> int:
    """
    Sum all the integers from ``0`` to ``integer``.

    ``integer`` must be a positive integer number, otherwise ``0``
    is returned.

    :param integer: positive integer number.
    :type integer: int
    :return: sum of all positive integers up to ``integer`` included;
        ``0`` if ``integer`` is not a positive integer.
    """

    if isinstance(integer, int) and integer >= 0:
        return sum(range(integer + 1))
    else:
        return 0


if __name__ == '__main__':
    assert add_it_up(0) == 0

    assert add_it_up(1) == 1

    assert add_it_up(5.6) == 0

    assert add_it_up(-5) == 0

    assert add_it_up(100) == 5050
