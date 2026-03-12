class Solution27 {
    fun removeElement(nums: IntArray, `val`: Int): Int {
        var k = 0

        for (i in nums.indices) {
            if (nums[i] != `val`) {
                nums[k] = nums[i]
                k++
            }
        }
        return k
    }
}