class Solution:
    def myAtoi(self, s: str) -> int:
        ans = ""
        fl = False
        for i in range(len(s)):
            if len(ans) == 0 and (s[i] == " " or s[i] == "0"):
                if s[i] == "0" and i + 1 < len(s) - 1 and s[i + 1] in "0123456789":
                    fl = True
                    continue
                elif s[i] == "0" and i + 1 < len(s) - 1 and s[i + 1] not in "0123456789":
                    return 0

                continue
            elif len(ans) == 0 and s[i] not in "+-123456789":
                return 0
            elif len(ans) != 0 and s[i] not in "0123456789":
                break
            else:
                if fl and s[i] in "+-":
                    break
                ans += s[i]

        try:
            ans = int(ans)
        except:
            return 0

        if ans > 2 ** 31 - 1:
            return 2 ** 31 - 1
        elif ans < -2 ** 31:
            return -2 ** 31

        return ans