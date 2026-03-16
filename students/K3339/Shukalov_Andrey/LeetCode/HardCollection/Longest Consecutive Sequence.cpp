class Solution {
public:
    int longestConsecutive(vector<int>& nums) {
        unordered_map<int, pair<int, bool>> numbers;
        int ans = 0;
        for (auto& i : nums) numbers[i] = {1, false};
        for (auto& i : numbers) {
            if (i.second.second) continue;
            int prev = i.first - 1;
            int cnt = 1;
            deque<int> vis;
            vis.push_back(i.first);
            while (numbers.contains(prev)) {
                if (numbers[prev].second) {
                    cnt += numbers[prev].first;
                    break;
                }
                vis.push_back(prev);
                cnt += 1;
                prev--;
            }
            while (!vis.empty()) {
                numbers[*vis.begin()] = {cnt--, true};
                vis.pop_front();
            }
        }
        for (auto& i : numbers) {
            ans = max(ans, i.second.first);
        }
        return ans;
    }
};
