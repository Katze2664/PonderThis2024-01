# https://research.ibm.com/haifa/ponderthis/challenges/January2024.html

# ??+??-??-??=5
#  +  +  -  +
# ??+??+??-??=10
#  +  -  -  +
# ??-??+??+??=9
#  -  -  +  +
# ??-??+??-??=0
#  =  =  =  =
# 17  8 11 48

# "[+,-,-,+,+,-,+,+,+,-,+,-,-,+,-,+,+,-,-,+,+,-,+,-]"

# %%

import numpy as np

def operator_parser(operator_str):
    operator_lst = []
    for char in operator_str:
        if char == "+":
            operator_lst.append(1)
        elif char == "-":
            operator_lst.append(-1)
    return operator_lst

def make_checker(operator_str, target, row=None, col=None):
    # Rows and cols are indexed from 0
    assert (row is None) != (col is None), "Must specify exactly one row or col"
    operator_lst = operator_parser(operator_str)
    if row is not None:
        ops = np.array([1] + operator_lst[7 * row : 7 * row + 3])
    if col is not None:
        ops = np.array([1] + operator_lst[col + 3 :: 7])
    
    def checker(board):
        if row is not None:
            nums = np.array(board[4 * row: 4 * row + 4])
        if col is not None:
            nums = np.array(board[col :: 4])
    
        return sum(nums * ops) == target
        
    return checker

def board_printer(board):
    result = np.array(board).reshape(4, 4)
    print(result)

# %%
operator_str = "[+,-,-,+,+,-,+,+,+,-,+,-,-,+,-,+,+,-,-,+,+,-,+,-]"

checker_row0 = make_checker(operator_str, 5, row=0)
checker_row1 = make_checker(operator_str, 10, row=1)
checker_row2 = make_checker(operator_str, 9, row=2)
checker_row3 = make_checker(operator_str, 0, row=3)
checker_col0 = make_checker(operator_str, 17, col=0)
checker_col1 = make_checker(operator_str, 8, col=1)
checker_col2 = make_checker(operator_str, 11, col=2)
checker_col3 = make_checker(operator_str, 48, col=3)

# %%
lst = list(range(1, 17))
print(checker_col2(lst))
board_printer(lst)

# %%
