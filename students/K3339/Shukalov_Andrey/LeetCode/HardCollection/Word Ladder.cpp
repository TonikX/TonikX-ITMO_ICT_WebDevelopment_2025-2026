class Solution {
public:
    int ladderLength(string beginWord, string endWord, vector<string>& wordList) {
        unordered_map<string, int> dist;
        unordered_set<string> used;
        unordered_set<string> words;
        for (auto& i : wordList) {
            words.insert(i);
        }
        if (!words.contains(endWord))
            return 0;
        dist[beginWord] = 1;
        deque<string> q;
        q.push_front(beginWord);
        while (!q.empty() && used.size() != wordList.size()) {
            auto curr = q.front();
            auto tmp = curr;
            q.pop_front();
            for (size_t i = 0; i < curr.size(); ++i) {
                for (char x = 'a'; x <= 'z'; ++x) {
                    if (x != tmp[i]) {
                        tmp[i] = x;
                        if (words.contains(tmp) && !used.contains(tmp)) {
                            dist[tmp] = dist[curr] + 1;
                            used.insert(tmp);
                            q.push_back(tmp);
                            if (tmp == endWord) {
                                return dist[tmp];
                            }
                        }
                        tmp[i] = curr[i];
                    }
                }
            }
        }
        return 0;
    }
};