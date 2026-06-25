import numpy as np

def reverse_list(l: list):
    """
    Reverse a list without using any built-in functions.
    The function should return a reversed list.
    Input l is a list that may contain any type of data.
    """
    left = 0
    right = len(l) - 1
    while left < right:
        l[left], l[right] = l[right], l[left]
        left += 1
        right -= 1
    return l


print(reverse_list([]))
print(reverse_list([1, 2, 3, 4, 5]))
print(reverse_list(["a", "b", "c", "d", "e"]))
print(reverse_list([1.5, 2.5, 3.5, 4.5, 5.5]))
print(reverse_list([1, "hello", 2, True, 9.7, [1, 2], (3, 4)]))
print(reverse_list([[1, 2], [3, 4], [5, 6]]))


def solve_sudoku(matrix):
    """
    Write a program to solve a 9x9 Sudoku board.
    The board must be completed so that every row, column, and 3x3 section
    contains all digits from 1 to 9.
    Input: a 9x9 matrix representing the board.
    """
    def is_valid(row, col, num):
        for i in range(9):
            if matrix[row][i] == num:
                return False
            if matrix[i][col] == num:
                return False
        section_row = row // 3
        section_col = col // 3
        for i in range(3):
            for j in range(3):
                if matrix[section_row*3+i][section_col*3+j] == num:
                    return False
        return True
    def solve():
        for i in range(9):
            for j in range(9):
                if matrix[i][j] == 0:
                    for num in range(1, 10):
                        if is_valid(i, j, num):
                            matrix[i][j] = num
                            if solve():
                                return True
                            matrix[i][j] = 0
                    return False
        return True

    if solve():
        print(np.matrix(matrix))
    else:
        print("No solution found")

# Test case 1 (solvable)
solve_sudoku([
    [5, 3, 0, 0, 7, 0, 0, 0, 0], 
    [6, 0, 0, 1, 9, 5, 0, 0, 0], 
    [0, 9, 8, 0, 0, 0, 0, 6, 0], 
    [8, 0, 0, 0, 6, 0, 0, 0, 3], 
    [4, 0, 0, 8, 0, 3, 0, 0, 1], 
    [7, 0, 0, 0, 2, 0, 0, 0, 6], 
    [0, 6, 0, 0, 0, 0, 2, 8, 0], 
    [0, 0, 0, 4, 1, 9, 0, 0, 5], 
    [0, 0, 0, 0, 8, 0, 0, 7, 9]])

# Test case 2 (solvable)
solve_sudoku([
    [0, 0, 0, 2, 6, 0, 7, 0, 1],
    [6, 8, 0, 0, 7, 0, 0, 9, 0],
    [1, 9, 0, 0, 0, 4, 5, 0, 0],
    [8, 2, 0, 1, 0, 0, 0, 4, 0],
    [0, 0, 4, 6, 0, 2, 9, 0, 0],
    [0, 5, 0, 0, 0, 3, 0, 2, 8],
    [0, 0, 9, 3, 0, 0, 0, 7, 4],
    [0, 4, 0, 0, 5, 0, 0, 3, 6],
    [7, 0, 3, 0, 1, 8, 0, 0, 0]])

# Test case 3 (unsolvable)
solve_sudoku([
    [5, 5, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]])