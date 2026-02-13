class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        ans = []
        for i in range(len(matrix)):
            temp = []
            for j in range(len(matrix) - 1, -1, -1):
                temp.append(matrix[j][i])

            ans.append(temp)

        for i in range(len(ans)):
            matrix[i] = ans[i]