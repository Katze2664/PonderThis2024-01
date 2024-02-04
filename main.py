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

def make_calc_last_num(operator_str, target, row=None, col=None):
    # Rows and cols are indexed from 0
    assert (row is None) != (col is None), "Must specify exactly one row or col"
    operator_lst = operator_parser(operator_str)
    if row is not None:
        ops = np.array([1] + operator_lst[7 * row : 7 * row + 3])
    if col is not None:
        ops = np.array([1] + operator_lst[col + 3 :: 7])
    
    def calc_last_num(board):
        if row is not None:
            nums = np.array(board[4 * row: 4 * row + 4])
        if col is not None:
            nums = np.array(board[col :: 4])

        last_num = (target - sum(nums[:3] * ops[:3])) / ops[3]
        return last_num
        
    return calc_last_num

def board_printer(board):
    result = np.array(board).reshape(4, 4)
    print(result)

# %%
operator_str = "[+,-,-,+,+,-,+,+,+,-,+,-,-,+,-,+,+,-,-,+,+,-,+,-]"

calc_last_num_row0 = make_calc_last_num(operator_str, 5, row=0)
calc_last_num_row1 = make_calc_last_num(operator_str, 10, row=1)
calc_last_num_row2 = make_calc_last_num(operator_str, 9, row=2)
calc_last_num_row3 = make_calc_last_num(operator_str, 0, row=3)
calc_last_num_col0 = make_calc_last_num(operator_str, 17, col=0)
calc_last_num_col1 = make_calc_last_num(operator_str, 8, col=1)
calc_last_num_col2 = make_calc_last_num(operator_str, 11, col=2)
calc_last_num_col3 = make_calc_last_num(operator_str, 48, col=3)

# %%
lst = list(range(1, 17))
print(calc_last_num_row0(lst))
print(calc_last_num_row1(lst))
print(calc_last_num_row2(lst))
print(calc_last_num_row3(lst))

print(calc_last_num_col0(lst))
print(calc_last_num_col1(lst))
print(calc_last_num_col2(lst))
print(calc_last_num_col3(lst))

board_printer(lst)

# %%
def backtrack(board, unused):
    print(board, unused)
    if len(unused) == 0:
        return board
    
    position = 16 - len(unused)
    if position in [1, 2, 3, 5, 6, 7, 9, 10, 11]:
        for num in unused:
            board_copy = board.copy()
            board_copy[position] = num
            unused_copy = unused.copy()
            unused_copy.remove(num)
            solution = backtrack(board_copy, unused_copy)
            if solution:
                return solution
    
    elif position in [4, 8]:
        if position == 4:
            num = calc_last_num_row0(board)
        else:
            num = calc_last_num_row1(board)
        board_copy = board.copy()
        board_copy[position] = num
        unused_copy = unused.copy()
        unused_copy.remove(num)
        solution = backtrack(board_copy, unused_copy)
        if solution:
            return solution

    elif position == 12:
        num12 = calc_last_num_row2(board)
        num13 = calc_last_num_col0(board)
        num14 = calc_last_num_col1(board)
        num15 = calc_last_num_col2(board)


        board_copy = board.copy()
        board_copy[12] = num12
        board_copy[13] = num13
        board_copy[14] = num14
        board_copy[15] = num15
        unused_copy = unused.copy()
        unused_copy.remove(num12)
        unused_copy.remove(num13)
        unused_copy.remove(num14)
        unused_copy.remove(num15)
        solution = backtrack(board_copy, unused_copy)
        if solution:
            return solution
        


        board_copy = board.copy()
        board[position] = num
        unused_copy = unused.copy()
        unused_copy.remove(num)
        solution = backtrack(board_copy, unused_copy)


