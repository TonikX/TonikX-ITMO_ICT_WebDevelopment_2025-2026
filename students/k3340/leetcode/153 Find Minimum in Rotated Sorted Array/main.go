package main

func findRotateIndex(nums []int) int {
	if nums[0] <= nums[len(nums)-1] {
		return 0
	}
	l := 0
	h := len(nums) - 1
	for l <= h {
		mid := (l + h) / 2
		if mid == 0 {
			return 1
		}
		if nums[mid-1] > nums[mid] {
			return mid
		}
		if nums[mid] > nums[h] {
			l = mid + 1
		} else {
			h = mid - 1
		}
	}
	return 0
}

func findMin(nums []int) int {
	rotateIndex := findRotateIndex(nums)
	return nums[0+rotateIndex]
}
