#https://leetcode.com/explore/interview/card/top-interview-questions-easy/98/design/562/

class MinStack(object):

    def __init__(self):
        self.arr = []
        self.mini = []

    def push(self, val):
        self.arr.append(val)
        if not(self.mini):
            self.mini.append(val)
        else:
            self.mini.append(min(val, self.mini[-1]))
        

    def pop(self):
        self.arr.pop()
        self.mini.pop()
        

    def top(self):
        return self.arr[len(self.arr)-1]
        

    def getMin(self):
        return self.mini[-1]
        



minStack = MinStack()
minStack.push(-2)
minStack.push(0)
minStack.push(-3)
minStack.getMin()
minStack.pop()
minStack.top()
minStack.getMin(); 