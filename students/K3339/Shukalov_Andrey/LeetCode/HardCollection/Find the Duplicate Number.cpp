class Solution {
public:
    int findDuplicate(vector<int>& nums) {
        int l = -1, r = ranges::max(nums);
        while (r - l > 1) {
            int m = (r - l) / 2 + l;
            int x = countL(nums, m);
            if (x > m) {
                r = m;
            } else {
                l = m;
            }
        }
        return r;
    }
    int countL(const vector<int>& nums, int v) {
        int ans = 0;
        for (auto& i : nums) {
            if (i <= v) ans += 1;
        }
        return ans;
    }
};
