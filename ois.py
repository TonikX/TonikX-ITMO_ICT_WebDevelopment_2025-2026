# nums = [1,1,2]

# res = []
# k = 0
# for i in range(len(nums) - 1):
#     if nums[i] != nums[i+1]:
#         k += 1
#         res.append(nums[i])
# if nums[len(nums)-1] not in res:
#     res.append(nums[len(nums)-1])
#     k += 1
# if len(nums) > len(res):
#     n = len(nums) - len(res)
#     res.extend(["_"] * n)
# print(k, res)


def removeDuplicates(nums: list[int]) -> int:
        k = 0
        for i in range(1, len(nums)):
            if nums[i] != nums[k]:
                k +=1
                nums[k] = nums[i]
        