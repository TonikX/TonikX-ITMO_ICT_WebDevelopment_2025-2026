class Solution {
public:
    int firstMissingPositive(vector<int>& nums) {
        bool flag = false;
        for (auto& i : nums) {
            if (i == 1) flag = true;
            if (i <= 0) i = 1;
        }
        if (!flag) return 1;
        for (int i = 0; i < nums.size(); ++i) {
            int x = abs(nums[i]);
            if (x <= nums.size() && nums[x - 1] > 0)
                nums[x - 1] = -nums[x - 1];
        }
        int mex = 2;
        for (int i = 1; i < nums.size(); ++i) {
            if (nums[i] > 0) break;
            mex++;
        }
        return mex;
    }
};
