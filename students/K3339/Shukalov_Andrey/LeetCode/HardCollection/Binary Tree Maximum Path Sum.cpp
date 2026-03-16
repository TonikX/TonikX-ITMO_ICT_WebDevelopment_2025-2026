class Solution {
public:
    int dfs(TreeNode* v) {
        int cnt1 = 0, cnt2 = 0;
        if (v->left) {
            cnt1 = dfs(v->left);
        }
        if (v->right) {
            cnt2 = dfs(v->right);
        }
        int ans = max(0, max(cnt1, cnt2)) + v->val;
        if (cnt1 >= 0 && cnt2 >= 0) {
            cost = max(cost, v->val + cnt1 + cnt2);
        } else if (cnt1 >= 0){
            cost = max(cost, v->val + cnt1);
        } else if (cnt2 >= 0) {
            cost = max(cost, v->val + cnt2);
        } else {
            cost = max(cost, v->val);
        }
        return ans;
    }

    int maxPathSum(TreeNode* root) {
        dfs(root);
        return cost;
    }
private:
    int cost{INT32_MIN};
};
