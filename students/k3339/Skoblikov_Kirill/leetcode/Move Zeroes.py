class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        zeros = []
        other = []
        for i in reversed(nums):
            if i == 0:
                zeros.append(i)
                nums.pop()
            else:
                other.append(i)
                nums.pop()

        for i in reversed(other):
            nums.append(i)

        for i in range(len(zeros)):
            nums.append(0)