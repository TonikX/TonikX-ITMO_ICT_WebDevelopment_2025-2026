class Solution81 {
    fun removeDuplicates(nums: IntArray): Int {
        var c = 0
        var n = -10001
        var k = 0
        for (i in nums.indices) {
            if (nums[i] != n) c = 0
            if (c < 2) {
                n = nums[i]
                c++
                nums[k] = nums[i]
                k++
            }
            return k
        }
    }
}