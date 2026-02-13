class Solution:
    def firstUniqChar(self, s: str) -> int:
        d = {}
        for i in range(len(s)):
            if s[i] not in d:
                d[s[i]] = [i]
            else:
                d[s[i]].append(i)

        ans = 9999999999999
        for v in d.values():
            if len(v) == 1 and ans > v[0]:
                ans = v[0]

        if ans == 9999999999999:
            return -1

        return ans