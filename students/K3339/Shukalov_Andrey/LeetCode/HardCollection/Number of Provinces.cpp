class Solution {
public:
    vector<int> used;
    void dfs(int v, int c, const vector<vector<int>>& mass) {
        used[v] = c;
        for (int i = 0; i < used.size(); ++i) {
            if (used[i] == 0 && mass[v][i] == 1) {
                dfs(i, c, mass);
            }
        }
    }
    int findCircleNum(vector<vector<int>>& isConnected) {
        used.resize(isConnected.size(), 0);
        int c = 1;
        for (int i = 0; i < isConnected.size(); ++i) {
            if (used[i] == 0) {
                dfs(i, c++, isConnected);
            }
        }
        return c - 1;
    }
};
