class Solution:
    def intersect(self, nums1: List[int], nums2: List[int]) -> List[int]:
        if len(nums1) < len(nums2):
            temp = nums2
            nums2 = nums1
            nums1 = temp

        d1 = {}
        d2 = {}
        for i in range(len(nums2)):
            if nums1[i] not in d1:
                d1[nums1[i]] = 1
            else:
                d1[nums1[i]] += 1

            if nums2[i] not in d2:
                d2[nums2[i]] = 1
            else:
                d2[nums2[i]] += 1

        for i in range(len(nums2), len(nums1)):
            if nums1[i] not in d1:
                d1[nums1[i]] = 1
            else:
                d1[nums1[i]] += 1

        ans = []
        for k, v in d2.items():
            if k not in d1:
                continue

            it = min(v, d1[k])
            for i in range(it):
                ans.append(k)

        return ans