class Solution26 {
    fun removeDuplicates(nums: IntArray): Int {
        var k = 0
        var uni = -1001
        var u = 0

        for (i in nums.indices) {
            if (nums[i] != uni) {
                uni = nums[i]
                nums[k++] = nums[i]
                u++
            }
        }
        return u
    }
}