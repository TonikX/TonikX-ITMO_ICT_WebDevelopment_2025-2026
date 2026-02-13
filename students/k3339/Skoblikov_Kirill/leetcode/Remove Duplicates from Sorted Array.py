class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        temp = sorted(list(set(nums)))
        for i in range(len(temp)):
            nums[i] = temp[i]

        return len(temp)