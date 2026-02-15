# https://leetcode.com/explore/interview/card/top-interview-questions-easy/99/others/565/
import math
class Solution(object):
    def hammingWeight(self, n):
        x,binary,cnt = int(math.log(n,2)),0,0
        while x >= 0:
            if binary + 2**x <= n:
                binary = binary + 2**x 
                cnt += 1
            x -= 1
        return cnt
        


sol = Solution()
print(sol.hammingWeight(536870912))