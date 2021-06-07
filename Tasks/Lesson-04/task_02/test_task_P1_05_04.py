"""
Написать тесты для домашних работ из курса «Python 1»
"""

import pytest
from task_P1_05_04 import roman


@pytest.mark.parametrize('num, result', [
    (5, 'V'),
    (10, 'X'),
    (112, 'CXII'),
    (1234, 'MCCXXXIV'),
    (34567, 'ẌẌẌMṼDLXVII'),
    (456789, 'ĈĎĹṼMDCCLXXXIX'),
])
def test_roman_list(num, result):
    assert roman(num) == result


def test_roman_single():
    assert roman(5) == 'V'

