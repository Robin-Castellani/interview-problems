README: problems solved in Python 🐍
=====================================

Here I show how I solve some problems that may be used as tests
in the recruitment process.
I got inspired from
`this article <https://realpython.com/python-practice-problems/>`_
on RealPython.

.. contents:: Table of contents

Dear recruiter... 👨‍💻👩‍💻
-----------------------------
I want to show you:

- how I solve problems with Python code
  (just trust I didn't had a peek at the solution before attempting 😉);
- I know how to style and write readable yet efficient and maintainable code;
- I know how to use Git and GitHub;
- I do have problem-solving skills and I do like solve problems;
- I do have analytical skills (by the way, I'm an engineer);
- I know how to write documentation with the ReStructuredText syntax
  (which I think is harder than Markdown, but it makes me obtain wonderful
  results without using LaTeX);
- I know how to use Sphinx and GitHub Actions to automatically build
  beautiful and professional documentation from docstrings;
- as you read, I speak (or better, I write) English.

The problems 🤔
------------------
Here is a list of all the problems I solved. Each problem is fully contained
in a file.

.. topic:: Requirements

  Python 3.8.5 and libraries in ``requirements.txt``, to be
  installed through ``pip install -r requirements.txt``
  (maybe in a virtual environment).

``1_integer_sum.py`` Sum a range of positive integers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Single function which ingests a number; if it is a positive integer,
return the sum of all positive integers from zero to that number included,
otherwise returns zero.

``2_caesar.py`` Encrypt or decrypt a string according to Caesar cipher
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Encrypt or decrypt a string by shifting the letters of ``n`` positions
in the alphabet; each non-letter character is preserved as it is.

Three versions are available, increasingly faster and more readable.

``3_logparse.py`` Parse a log and print a report
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Parse the ``test.log`` file looking for specific strings holding Device
status (``ON``, ``OFF`` or ``ERR``); print a report with the total ``ON``
time and the timestamps of ``ERR`` events.

``4_sudoku.py`` Classical Sudoku solver
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Read puzzles from a ``.sdm`` file and reports the solutions, if
they are unique.


Contributions 🙏
-------------------

Thank you for help me in improving the solutions!
If you have a better solution (faster, cleaner, more explicit, anything else),
please open an issue or a pull request, I'll be happy to discuss with you.

Whole new solutions will be added to the existing ones; the author will
be named in the docstring (no money, sorry).

Also, if you have any other interesting problem, you're welcome to submit it!


License 🔖
-------------

All the material in this repo is available through the
`Creative Commons Attribution-NonCommercial-ShareAlike
4.0 International license
<https://creativecommons.org/licenses/by-nc-sa/4.0/>`_.