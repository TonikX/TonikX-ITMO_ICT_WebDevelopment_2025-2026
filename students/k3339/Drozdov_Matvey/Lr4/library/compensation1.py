# https://leetcode.com/explore/interview/card/top-interview-questions-easy/99/others/722/

class Solution(object):
    def missingNumber(self, nums):
        nums = sorted(nums)
        all = [i for i in range(len(nums)+1)]
        for i in range(len(nums)):
            if all[i] != nums[i]:
                return all[i]
        return all[-1]
    
# sol = Solution()
# print(sol.missingNumber([9,6,4,2,3,5,7,0,1]))