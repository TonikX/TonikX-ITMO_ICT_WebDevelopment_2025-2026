#define pb push_back
#define pp pop_back
#define ff first
#define ss second

class Solution {
public:
    vector<int> spiralOrder(vector<vector<int>>& matrix) {
        int n = matrix.size();
        int m = matrix.begin()->size();
        vector<vector<bool>> used(n, vector<bool>(m, false));
        int all = n * m;
        pair<int, int> dir = {0, 1};
        pair<int, int> curr = {0, 0};
        vector<int> ans;
        while (all > 0) {
            ans.pb(matrix[curr.ff][curr.ss]);
            used[curr.ff][curr.ss] = true;
            if (!check(n, m, curr.ff, curr.ss, dir.ff, dir.ss) ||
                used[curr.ff + dir.ff][curr.ss + dir.ss]) {
                setDir(dir);
                }
            curr.ff += dir.ff;
            curr.ss += dir.ss;
            all--;
        }
        return ans;
    }
    bool check(int n, int m, int x, int y, int dx, int dy) {
        return x + dx >= 0 && x + dx < n && y + dy >= 0 && y + dy < m;
    }
    void setDir(pair<int, int>& dir) {
        if (dir.ss == 1) {
            dir.ss = 0;
            dir.ff = 1;
        } else if (dir.ff == 1) {
            dir.ss = -1;
            dir.ff = 0;
        } else if (dir.ss == -1) {
            dir.ss = 0;
            dir.ff = -1;
        } else {
            dir.ss = 1;
            dir.ff = 0;
        }
    }
};
