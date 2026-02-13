class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        prof = 0
        today = 0
        for i in range(len(prices)):
            if i < today:
                continue

            for j in range(i+1, len(prices)):
                if prices[j] < prices[i]:
                    today += 1
                    break

                maybe_prof = prices[j] - prices[i]
                if maybe_prof > 0:
                    prof += maybe_prof
                    today = j
                    break

        return prof