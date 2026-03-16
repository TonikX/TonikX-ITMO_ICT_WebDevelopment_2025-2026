class Solution {
public:
    int fourSumCount(vector<int>& nums1, vector<int>& nums2, vector<int>& nums3, vector<int>& nums4) {
        int ans = 0;
        map<int, int> cnt;
        for (int i = 0; i < nums3.size(); ++i) {
            for (int j = 0; j < nums4.size(); ++j) {
                cnt[nums3[i] + nums4[j]] += 1;
            }
        }

        for (int i = 0; i < nums1.size(); ++i) {
            for (int j = 0; j < nums2.size(); ++j) {
                int sum = nums1[i] + nums2[j];
                ans += cnt[-sum];
            }
        }

        return ans;
    }
};
