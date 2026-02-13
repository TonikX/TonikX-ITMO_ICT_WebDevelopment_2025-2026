class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        ans_d = {}
        for i in nums:
            if i not in ans_d:
                ans_d[i] = 1
            else:
                ans_d[i] += 1

        for k, v in ans_d.items():
            if v == 1:
                return k