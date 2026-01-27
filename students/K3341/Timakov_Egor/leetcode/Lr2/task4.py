###https://leetcode.com/explore/interview/card/top-interview-questions-hard/116/array-and-strings/827/
from typing import List


def productExceptSelf(nums: List[ int ]) -> List[int]:
    length = len(nums)
    answer = [1] * length
    left = 1
    right = 1
    for i in range(length):
        answer[i] = left
        left *= nums[i]


    for i in range(length-1,-1, -1):
        answer[i] *= right
        right *= nums[i]

    return answer


print(productExceptSelf([-1,1,0,-3,3]))