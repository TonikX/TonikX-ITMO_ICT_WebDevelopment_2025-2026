### https://leetcode.com/explore/interview/card/top-interview-questions-easy/92/array/727/
from typing import List


def removeDuplicates(nums: List [int]) -> int:

    i = 1

    while i < len(nums):
        if nums[i] == nums[i-1]:
            nums.pop(i-1)
        else:
            i += 1
    return nums


print(removeDuplicates([1, 1, 2]))