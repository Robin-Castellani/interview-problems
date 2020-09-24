"""
Caesar Cipher

A Caesar cipher is a simple substitution cipher in which each letter of the
plain text is substituted with a letter found by moving ``n`` places down the
alphabet.

For example, assume the input plain text is the following::

    abcd xyz

If the shift value, ``n``, is ``4``,
then the encrypted text would be the following::

    efgh bcd

You are to write a function that accepts two arguments, a plain-text
message and a number of letters to shift in the cipher. The function will
return an encrypted string with all letters transformed and all
punctuation and whitespace remaining unchanged.

..note::

  You can assume the plain text is all lowercase ASCII except for
  whitespace and punctuation.
"""

import string
import functools
import time


def timer(func):
    """
    Simple decorator to print how much time a function requires
    to run.
    """
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        tic = time.perf_counter()
        value = func(*args, **kwargs)
        toc = time.perf_counter()
        elapsed_time = toc - tic
        print(f"{func.__name__}: {elapsed_time * 10e6:0.0f} μseconds")
        return value
    return wrapper_timer


@timer
def cipher_caesar(text: str, n: int) -> str:
    """
    Encrypt or decrypt the letters in a string preserving all non
    letters characters (such as punctuation) according to the Caesar
    method: shift the letters of ``n`` position.

    :param text: string to be decrypted or encrypted.
    :param n: number of position to shift the letters.
    :return: decrypted/encrypted string.
    """

    # get the total number of lowercase letters
    TOTAL_ASCII_LOWERCASE = len(string.ascii_lowercase)
    # initialise the encrypted output string
    encrypted_text = ''
    # loop over all the characters of the input string
    for character in text:
        # perform the encryption only on lowercase letters
        if character in string.ascii_lowercase:
            char_position = string.ascii_lowercase.index(character)
            encrypted_char = string.ascii_lowercase[
                char_position + n - TOTAL_ASCII_LOWERCASE
            ]
            encrypted_text += encrypted_char
        # preserve the digits, punctuation and whitespaces
        else:
            encrypted_text += character

    return encrypted_text


@timer
def cipher_caesar_v2(text: str, n: int) -> str:
    """
    Second version of the using list comprehension. More concise.
    Slower on single letters, faster on longer strings than V1.

    Encrypt or decrypt the letters in a string preserving all non
    letters characters (such as punctuation) according to the Caesar
    method: shift the letters of ``n`` position.

    :param text: string to be decrypted or encrypted.
    :param n: number of position to shift the letters.
    :return: decrypted/encrypted string.
    """

    # get the total number of lowercase letters
    TOTAL_ASCII_LOWERCASE = len(string.ascii_lowercase)
    # perform the encryption only on lowercase letters
    # preserve the digits, punctuation and whitespaces
    list_str_encrypt = [
        string.ascii_lowercase[
            string.ascii_lowercase.index(character) + n - TOTAL_ASCII_LOWERCASE
        ]
        if character in string.ascii_lowercase else character
        for character in text
    ]
    encrypted_text = ''.join(list_str_encrypt)

    return encrypted_text


@timer
def cipher_caesar_v3(text: str, n: int) -> str:
    """
    Second version of the using ``str``'s ``translate`` function.
    Even more concise, slower on single characters but definitely
    faster than V2 on long strings.

    Encrypt or decrypt the letters in a string preserving all non
    letters characters (such as punctuation) according to the Caesar
    method: shift the letters of ``n`` position.

    :param text: string to be decrypted or encrypted.
    :param n: number of position to shift the letters.
    :return: decrypted/encrypted string.
    """

    # create a conversion table only for ascii letters
    conversion_table = text.maketrans(
        string.ascii_lowercase,
        string.ascii_lowercase[n:] + string.ascii_lowercase[:n]
    )
    # apply the conversion table to the input text
    encrypted_text = text.translate(conversion_table)

    return encrypted_text


if __name__ == '__main__':
    for letter in string.ascii_lowercase:
        assert cipher_caesar(letter, 0) == letter
        assert cipher_caesar_v2(letter, 0) == letter
        assert cipher_caesar_v3(letter, 0) == letter

    for dig in string.digits:
        assert cipher_caesar(dig, 10) == dig
        assert cipher_caesar_v2(dig, 10) == dig
        assert cipher_caesar_v3(dig, 10) == dig

    for punct in string.punctuation:
        assert cipher_caesar(punct, 1) == punct
        assert cipher_caesar_v2(punct, 1) == punct
        assert cipher_caesar_v3(punct, 1) == punct

    for whitespace in string.whitespace:
        assert cipher_caesar(whitespace, 7) == whitespace
        assert cipher_caesar_v2(whitespace, 7) == whitespace
        assert cipher_caesar_v3(whitespace, 7) == whitespace

    assert cipher_caesar('rkgerzr nhgbzngvba vf njrfbzr!', 13) == \
           'extreme automation is awesome!'

    assert cipher_caesar_v2('rkgerzr nhgbzngvba vf njrfbzr!', 13) == \
           'extreme automation is awesome!'

    assert cipher_caesar_v3('rkgerzr nhgbzngvba vf njrfbzr!', 13) == \
           'extreme automation is awesome!'
