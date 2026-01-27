### https://leetcode.com/explore/interview/card/top-interview-questions-medium/103/array-and-strings/780/

def center(left, right, s):
    while left >= 0 and right < len(s) and s[left] == s[right]:
        left -= 1
        right +=1
    return s[left + 1:right]
def longestPaindrome(s: str) -> str:
    if len(s) <=1:
        return s
    long = ''

    for i in range(len(s)):
        pal_odd = center(i, i, s)
        pal_even = center(i, i+1, s)

        long = max(long, pal_odd, pal_even, key=len)

    return long



print(longestPaindrome('babad'))