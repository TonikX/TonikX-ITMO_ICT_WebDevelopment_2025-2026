class Solution122 {
    fun maxProfit(prices: IntArray): Int {
        var sumProfit = 0

        for (i in 1 until prices.size) {
            if (prices[i] > prices[i - 1])
                sumProfit += prices[i] - prices[i - 1]
        }
        return sumProfit
    }

}