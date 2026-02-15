# https://leetcode.com/explore/interview/card/top-interview-questions-easy/102/math/745/

class Solution(object):
    def isPowerOfThree(self, n):
        x = 0
        while 3 ** x <= n:
            if 3 ** x == n:
                return True
            x += 1
        return False
