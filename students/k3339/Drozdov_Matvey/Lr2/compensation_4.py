# https://leetcode.com/explore/interview/card/top-interview-questions-easy/94/trees/555/

class Solution(object):
    def maxDepth(self, root):
        if not root:
            return 0
        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))
