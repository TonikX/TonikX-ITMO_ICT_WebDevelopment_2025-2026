class Solution {
public:
    int strStr(string haystack, string needle) {
        if (needle.empty()) return 0;
        for (int i = 0; i <= (int)haystack.size() - (int)needle.size(); ++i) {
            if (haystack.substr(i, needle.size()) == needle) {
                return i;
            }
        }
        return -1;
    }
};
