class Solution {
public:
    int myAtoi(string s) {
        int i = 0, n = s.size();
        long res = 0;
        int sign = 1;
        while (i < n && s[i] == ' ') i++;
        if (i < n && (s[i] == '+' || s[i] == '-')) {
            sign = (s[i++] == '-') ? -1 : 1;
        }
        while (i < n && isdigit(s[i])) {
            res = res * 10 + (s[i++] - '0');
            if (res > INT_MAX) {
                return (sign == 1) ? INT_MAX : INT_MIN;
            }
        }
        return sign * res;
    }
};
