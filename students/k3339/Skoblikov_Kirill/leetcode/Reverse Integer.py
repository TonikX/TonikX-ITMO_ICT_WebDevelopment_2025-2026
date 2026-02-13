class Solution:
    def reverse(self, x: int) -> int:
        ans = ''
        if x < 0:
            ans += '-'
            x *= -1

        x = str(x)

        for i in reversed(x):
            ans += i

        if int(ans) > 2 ** 31 - 1 or int(ans) < -2 ** 31:
            return 0

        return int(ans)