#https://leetcode.com/explore/interview/card/top-interview-questions-easy/127/strings/882/

class Solution(object):
    def isAnagram(self, s, t):
        if len(s) != len(t):
            return False

        cnt = {}
        for ch in s:
            cnt[ch] = cnt.get(ch, 0) + 1

        for ch in t:
            if ch not in cnt:
                return False
            cnt[ch] -= 1
            if cnt[ch] == 0:
                del cnt[ch]

        return not cnt