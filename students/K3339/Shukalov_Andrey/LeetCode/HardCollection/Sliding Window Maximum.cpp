class Solution {
public:
    vector<int> maxSlidingWindow(vector<int>& ls, int k) {
        int x = ls.size(), y = k;
        vector<pair<int, int>> a, b;
        vector<int> ans;
        int c = ls[0];
        for(int i = 0; i < y; i++)
        {
            if(ls[i] < c)
                c = ls[i];
            a.push_back(make_pair(ls[i], c));
        }
        //ans.push_back(a[a.size() - 1].second);
        int mxx = INT32_MIN;
        for (int q = 0; q < k; ++q)
            mxx = max(mxx, ls[q]);
        ans.push_back(mxx);

        for(int j = y; j < x; j++)
        {
            int q = a.size();
            if(b.size() == 0)
                for(int t = 0; t < q; t++){
                    if(t == 0)
                        b.push_back(make_pair(a[a.size() - 1].first, a[a.size() - 1].first));
                    else
                        b.push_back(make_pair(a[a.size() - 1].first, max(a[a.size() - 1].first, b[b.size() - 1].second)));
                    a.pop_back();
                }
            b.pop_back();
            pair<int, int> s = make_pair(ls[j],ls[j]);
            if(a.size() != 0)
                s.second = max(a[a.size() - 1].second, ls[j]);
            a.push_back(s);
            if(b.size() == 0)
                ans.push_back(a[a.size() - 1].second);
            else
                ans.push_back(max(a[a.size() - 1].second, b[b.size() - 1].second));
        }
        return ans;
    }
};
