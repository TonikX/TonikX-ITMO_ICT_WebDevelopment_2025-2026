package main

func firstTargetSearch(nums []int, target int) int {
	l := 0
	h := len(nums) - 1
	firstTargetPos := -1
	for l <= h {
		mid := (l + h) / 2
		if nums[mid] == target {
			firstTargetPos = mid
			h = mid - 1
		} else if nums[mid] > target {
			h = mid - 1
		} else {
			l = mid + 1
		}
	}
	return firstTargetPos
}

func lastTargetSearch(nums []int, target int) int {
	l := 0
	h := len(nums) - 1
	lastTargetPos := -1
	for l <= h {
		mid := (l + h) / 2
		if nums[mid] == target {
			lastTargetPos = mid
			l = mid + 1
		} else if nums[mid] > target {
			h = mid - 1
		} else {
			l = mid + 1
		}
	}
	return lastTargetPos
}

func searchRange(nums []int, target int) []int {
	return []int{firstTargetSearch(nums, target), lastTargetSearch(nums, target)}
}
