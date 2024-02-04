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

# Solution
# [2, 14, 4, 7, 12, 8, 5, 15, 9, 11, 1, 10, 6, 3, 13, 16]

#  2 + 14 -  4 -  7 =  5
#  +    +    -    +
# 12 +  8 +  5 - 15 = 10
#  +    -    -    +
#  9 - 11 +  1 + 10 =  9
#  -    -    +    +
#  6 -  3 + 13 - 16 =  0
#  =    =    =    =
# 17    8   11   48

# %%

import numpy as np
import time

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
        return int(last_num)
        
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
def backtrack(board, unused_set):
    unused_list = list(unused_set)
    
    position = 16 - len(unused_list)

    if position in [0, 4, 8]:
        ijk = ((i, j, k) for i in range(len(unused_list))
                         for j in range(len(unused_list)) if j != i
                         for k in range(len(unused_list)) if k != i and k != j)

        for i, j, k in ijk:
            num0, num1, num2 = unused_list[i], unused_list[j], unused_list[k]
            nums = [num0, num1, num2]
            board[position : position + 3] = nums
            if position == 0:
                last_num = calc_last_num_row0(board)
            elif position == 4:
                last_num = calc_last_num_row1(board)
            else:
                assert position == 8
                last_num = calc_last_num_row2(board)
            
            if last_num in unused_set and last_num not in nums:
                board[position + 3] = last_num
                unused_set_copy = unused_set.copy()
                for num in [num0, num1, num2, last_num]:
                    unused_set_copy.remove(num)
                solution = backtrack(board, unused_set_copy)
                if solution:
                    return solution       

    else:
        assert position == 12
        num12 = calc_last_num_col0(board)
        num13 = calc_last_num_col1(board)
        num14 = calc_last_num_col2(board)
        num15 = calc_last_num_col3(board)

        nums = [num12, num13, num14, num15]
        if set(nums) == unused_set:
            board[position : position + 4] = nums

            if calc_last_num_row3(board) == num15:
                # print("Solution found!", board)
                return board
    
    return False

# %%
start_time = time.time()
board = [0] * 16
unused_set = set(range(1, 17))
solution = backtrack(board, unused_set)
print(solution)
print(time.time() - start_time)
# %%
