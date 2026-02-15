# https://leetcode.com/explore/interview/card/top-interview-questions-easy/99/others/601/

class Solution(object):
    def generate(self, numRows):
        if numRows == 1:
            res = [[1]]

        elif numRows == 2:
            res = [[1], [1, 1]]

        else:
            res = [[1], [1, 1]]
            while len(res) != numRows:
                arr = [1]
                for i in range(len(res[-1]) - 1):
                    arr.append(res[-1][i] + res[-1][i + 1])
                arr.append(1)
                res.append(arr)
        return res
    
print (Solution().generate(5))
        
        