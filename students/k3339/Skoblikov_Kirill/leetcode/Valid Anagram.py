class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False

        d1 = {}
        d2 = {}
        for i in range(len(s)):
            if s[i] not in d1:
                d1[s[i]] = 1
            else:
                d1[s[i]] += 1

            if t[i] not in d2:
                d2[t[i]] = 1
            else:
                d2[t[i]] += 1

        if d1 == d2:
            return True
        else:
            return False