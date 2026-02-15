# https://leetcode.com/explore/interview/card/top-interview-questions-easy/92/array/674/

class Solution(object):
    def intersect(self, nums1, nums2):
        dictionary = dict()
        res = []
        if len(nums1) <= len(nums2):
            for n in nums2:
                dictionary[n] = dictionary.get(n,0) + 1
            for n in nums1:
                if n in dictionary.keys() and dictionary[n] != 0:
                    dictionary[n]-=1
                    res.append(n)
        else:
            for n in nums1:
                dictionary[n] = dictionary.get(n,0) + 1
            
            for n in nums2:
                if n in dictionary.keys() and dictionary[n] != 0:
                    dictionary[n]-=1
                    res.append(n)
        return res
    

print(Solution().intersect(nums1 = [3,1,2], nums2 = [1,1]))
    
