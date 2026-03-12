class Solution189 {
    fun rotate(nums: IntArray, k: Int): Unit {
        val n = nums.size
        val k = k % n

        reverse(nums, 0, n - 1)
        reverse(nums, 0, k)
        reverse(nums, k, n - 1)

    }

    fun reverse(nums: IntArray, left: Int, right: Int): Unit {

        var l = left
        var r = right

        while (l < r) {
            val temp = nums[l]
            nums[l] = nums[r]
            nums[r] = temp
            l++
            r--
        }
    }
}