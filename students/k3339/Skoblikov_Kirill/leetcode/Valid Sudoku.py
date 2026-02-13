class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        columns = []
        for i in range(9):
            temp = []
            for j in range(9):
                temp.append(board[j][i])

            columns.append(temp)

        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                if not (isValidSquare(board, i, j)):
                    return False

        for i in range(9):
            if not (isValidLine(board[i])) or not (isValidLine(columns[i])):
                return False

        return True


def isValidSquare(square, a, b):
    d = {i: 0 for i in range(1, 10)}
    for i in range(3):
        for j in range(3):
            if square[a + i][b + j] in "123456789":
                d[int(square[a + i][b + j])] += 1

    for v in d.values():
        if v > 1:
            return False

    return True


def isValidLine(line):
    d = {i: 0 for i in range(1, 10)}
    for i in range(9):
        if line[i] in "123456789":
            d[int(line[i])] += 1

    for v in d.values():
        if v > 1:
            return False

    return True