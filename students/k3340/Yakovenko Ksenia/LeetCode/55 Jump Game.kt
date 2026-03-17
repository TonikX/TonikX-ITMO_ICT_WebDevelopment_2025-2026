class Solution55 {
    fun canJump(nums: IntArray): Boolean {
        var maxDestination = 0
        for (i in nums.indices) {
            if (i <= maxDestination) {
                if ((i + nums[i]) > maxDestination) {
                    maxDestination = i + nums[i]
                }
            }
            else return false
        }
        return true
    }
}