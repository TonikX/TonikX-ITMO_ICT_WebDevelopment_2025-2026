#https://leetcode.com/explore/interview/card/top-interview-questions-easy/92/array/567/

class Solution(object):
    def moveZeroes(self, nums):
        j = 0
        for i in range(len(nums)):
            if nums[i] != 0 and nums[j] == 0:
                nums[j] = nums[i]
                nums[i] = 0
                j+=1
            if (j+1) <= len(nums)-1 and nums[j] != 0:
                j += 1 
        return nums
    
