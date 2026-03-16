class Solution {
public:
  int dfs(TreeNode* v, TreeNode* p, TreeNode* q) {
    int cnt = 0;
    if (v->left) {
      cnt += dfs(v->left, p, q);
    }
    if (v->right) {
      cnt += dfs(v->right, p, q);
    }
    if (v == p) cnt++;
    if (v == q) cnt++;
    if (cnt == 2) {
      if (!set) {
        ans = v;
        set = true;
      }
    }
    return cnt;
  }

  TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
    dfs(root, p, q);
    return ans;
  }
private:
  bool set{false};
  TreeNode* ans{NULL};
};
