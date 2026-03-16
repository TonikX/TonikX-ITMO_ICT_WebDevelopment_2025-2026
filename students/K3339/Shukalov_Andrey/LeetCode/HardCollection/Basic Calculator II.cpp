class Solution {
public:
    int calculate(string s) {
        deque <char> op;
        deque <int> numbers;
        int currNum = 0;
        for (auto& i : s) {
            if (i == ' ') continue;
            if (i == '+' || i == '-' || i == '*' || i == '/') {
                if (!op.empty() && (op.back() == '*' || op.back() == '/')) {
                    int x = numbers.back();
                    int oopp = op.back();
                    op.pop_back();
                    numbers.pop_back();
                    if (oopp == '*') {
                        numbers.push_back(x * currNum);
                    } else {
                        numbers.push_back(x / currNum);
                    }
                } else {
                    numbers.push_back(currNum);
                }
                op.push_back(i);
                currNum = 0;
            } else {
                currNum *= 10;
                currNum += (i - '0');
            }
        }
        if (!op.empty() && (op.back() == '*' || op.back() == '/')) {
            int x = numbers.back();
            int oopp = op.back();
            op.pop_back();
            numbers.pop_back();
            if (oopp == '*') {
                numbers.push_back(x * currNum);
            } else {
                numbers.push_back(x / currNum);
            }
        } else {
            numbers.push_back(currNum);
        }
        while (!op.empty()) {
            int x = numbers.front();
            numbers.pop_front();
            int y = numbers.front();
            numbers.pop_front();
            int oopp = op.front();
            op.pop_front();
            if (oopp == '+') {
                numbers.push_front(x + y);
            } else {
                numbers.push_front(x - y);
            }
        }
        return numbers.front();
    }
};
