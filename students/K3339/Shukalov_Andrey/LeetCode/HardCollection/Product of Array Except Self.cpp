class Solution {
public:
    vector<int> productExceptSelf(vector<int>& nums) {
        int n = nums.size();
        vector<int> ret(n);
        vector<int> pref(n, 0);
        vector<int> suff(n, 0);
        pref[0] = nums[0];
        suff[n - 1] = nums[n - 1];
        for (int i = 1; i < n; ++i) {
            pref[i] = pref[i - 1] * nums[i];
        }
        for (int i = n - 2; i >= 0; --i) {
            suff[i] = suff[i + 1] * nums[i];
        }
        for (int i = 0; i < n; ++i) {
            if (i == 0) {
                ret[i] = suff[1];
            } else if (i == n - 1) {
                ret[i] = pref[n - 2];
            } else {
                ret[i] = suff[i + 1] * pref[i - 1];
            }
        }
        return ret;
    }
};
