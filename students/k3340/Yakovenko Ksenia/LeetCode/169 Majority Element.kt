class Solution169 {
    fun majorityElement(nums: IntArray): Int {
        var c = 0
        var votes = 0
        for (i in nums.indices) {
            if (votes == 0) c = nums[i]
            if (nums[i] == c) {
                votes ++
            } else votes--
        }
        return c
    }
}