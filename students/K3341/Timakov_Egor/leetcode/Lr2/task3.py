### https://leetcode.com/explore/interview/card/top-interview-questions-hard/116/array-and-strings/830/
from typing import List


def maxArea(height: List[int]) -> int:
    maximum_area = -1
    left = 0
    right = len(height) - 1

    while left < right:
        h = min(height[left], height[right])
        width = right - left
        area = h*width
        maximum_area = max(maximum_area, area)

        if height[left] > height[right]:
            right -= 1
        else:
            left += 1

    return maximum_area


print(maxArea([1, 1]))