### https://leetcode.com/explore/interview/card/top-interview-questions-medium/103/array-and-strings/781/
from typing import List


def increasingTriplet(nums: List[int]) -> bool:
    first = 2**31
    second = 2*31
    for i in nums:
        if i <= first:
            first = i
        elif i <= second:
            second = i
        else:
            return True
    return False


print(increasingTriplet([2, 1, 5, 0, 4, 6]))