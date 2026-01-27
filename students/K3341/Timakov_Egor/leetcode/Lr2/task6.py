### https://leetcode.com/explore/interview/card/top-interview-questions-easy/92/array/549/
from typing import List


def singleNumber( nums: List[int]) -> int:

    result = 0
    for i in nums:
        result ^= i
    return result


print(singleNumber([4,1,2,1,2]))