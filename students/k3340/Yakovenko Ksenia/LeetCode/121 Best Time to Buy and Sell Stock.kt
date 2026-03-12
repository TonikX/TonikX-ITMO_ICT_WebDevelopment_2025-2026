class Solution121 {
    fun maxProfit(prices: IntArray): Int {
        var buy = Int.MAX_VALUE
        var maxProfit = 0

        for (i in prices.indices) {
            if (prices[i] < buy)
                buy = prices[i]
            if (maxProfit < prices[i] - buy)
                maxProfit = prices[i] - buy
        }
        return maxProfit
    }

}