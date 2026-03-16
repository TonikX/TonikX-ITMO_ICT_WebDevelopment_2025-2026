class Solution {
public:
    int maxArea(vector<int>& height) {
        int n = height.size();
        int l = 0, r = n - 1;
        int ans = INT32_MIN;
        while (l <= r) {
            int x = (r - l) * min(height[l], height[r]);
            if ((r - l) * min(height[l], height[r]) > ans) {
                ans = (r - l) * min(height[l], height[r]);
            }
            if (height[l] < height[r]) {
                l++;
            } else {
                r--;
            }
        }
        return ans;
    }
};
