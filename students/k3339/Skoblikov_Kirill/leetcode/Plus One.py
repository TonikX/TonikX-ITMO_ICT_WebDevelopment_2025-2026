class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        ost = (digits[-1] + 1) % 10
        k = -1
        digits[-1] = (digits[-1] + 1) % 10
        while ost == 0:
            if abs(k) == len(digits):
                ost = 1
                digits.insert(0, 1)
                break

            ost = (digits[-1 + k] + 1) % 10
            digits[-1 + k] = (digits[-1 + k] + 1) % 10
            k -= 1

        return digits