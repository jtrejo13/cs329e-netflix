#!/usr/bin/env python3

# -------
# imports
# -------
from Netflix import netflix_eval
from unittest import main, TestCase
from math import sqrt
from io import StringIO
from numpy import sqrt, square, mean, subtract


# -----------
# TestNetflix
# -----------

class TestNetflix (TestCase):

    # ----
    # eval
    # ----

    def test_eval_1(self):
        r = StringIO("1000:\n2326571\n977808\n1010534\n1861759\n")
        w = StringIO()
        netflix_eval(r, w)
        self.assertEqual(
            w.getvalue(), "1000:\n3.33\n3.33\n2.83\n4.33\n0.58\n")

    def test_eval_2(self):
        r = StringIO("1000:\n2326571\n977808\n1010534\n1861759\n10:\n1952305\n1531863\n")
        w = StringIO()
        netflix_eval(r, w)
        self.assertEqual(
            w.getvalue(), "1000:\n3.33\n3.33\n2.83\n4.33\n10:\n3.00\n3.00\n0.47\n")

    def test_eval_3(self):
        r = StringIO("10003:\n1515111\n")
        w = StringIO()
        netflix_eval(r, w)
        self.assertEqual(
            w.getvalue(), "10003:\n3.00\n0.0\n")

# ----
# main
# ----			
if __name__ == '__main__':
    main()

""" #pragma: no cover
% coverage3 run --branch TestNetflix.py >  TestNetflix.out 2>&1



% coverage3 report -m                   >> TestNetflix.out



% cat TestNetflix.out
.
----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
Name             Stmts   Miss Branch BrPart  Cover   Missing
------------------------------------------------------------
Netflix.py          27      0      4      0   100%
TestNetflix.py      13      0      0      0   100%
------------------------------------------------------------
TOTAL               40      0      4      0   100%

"""
