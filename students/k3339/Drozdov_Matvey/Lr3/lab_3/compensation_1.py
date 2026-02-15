#https://leetcode.com/explore/interview/card/top-interview-questions-easy/127/strings/881/

class Solution(object):
    def firstUniqChar(self, s):
        cnt = {}
        for ch in s:
            cnt[ch] = cnt.get(ch, 0) + 1

        for i, ch in enumerate(s):
            if cnt[ch] == 1:
                return i
        return -1