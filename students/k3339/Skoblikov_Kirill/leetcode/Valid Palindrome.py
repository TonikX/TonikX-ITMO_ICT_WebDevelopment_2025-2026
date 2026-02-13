class Solution:
    def isPalindrome(self, s: str) -> bool:
        abc = "qwertyuiopasdfghjklzxcvbnm1234567890"
        s = s.lower()
        new_s = ""
        for i in s:
            if i in abc:
                new_s += i

        for i in range(len(new_s) // 2):
            if new_s[i] != new_s[-1 - i]:
                return False

        return True