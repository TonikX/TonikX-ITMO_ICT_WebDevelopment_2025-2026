# https://leetcode.com/explore/interview/card/top-interview-questions-easy/99/others/648/
import math
class Solution(object):
    def reverseBits(self, n):
        res = 0
        new_n = 0
        pos = 31
        i = 31
        if n == 0:
            return 0
        attempt = int(math.log(n,2))
        if 2**attempt == n:
            return 2 ** (pos-attempt)
        
        while pos >= 0:
            if new_n + 2**pos <= n:
                new_n = new_n + 2**pos
                res += 2**(i - pos)
            pos -= 1

        return res
    
sol = Solution()
print(sol.reverseBits(2147483644))
        