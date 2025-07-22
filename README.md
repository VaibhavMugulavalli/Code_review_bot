# Code_review_bot
Small project built as part of my internship at ThoughtClan Technologies.
Utilizes gemini to review leetcode style question in either python or c++

================================== Test Cases ============================
Question:
Leetcode 1: Two Sum
Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.
Solution:
def twoSum(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]

Question:
Leetcode 200: Number of Islands
Given a 2D grid map of '1's (land) and '0's (water), count the number of islands.
Solution:
class Solution {
public:
    void dfs(vector<vector<char>>& grid, int i, int j) {
        if (i < 0 || j < 0 || i >= grid.size() || j >= grid[0].size() || grid[i][j] == '0')
            return;
        grid[i][j] = '0';
        dfs(grid, i+1, j);
        dfs(grid, i-1, j);
        dfs(grid, i, j+1);
        dfs(grid, i, j-1);
    }
    int numIslands(vector<vector<char>>& grid) {
        int count = 0;
        for (int i = 0; i < grid.size(); ++i) {
            for (int j = 0; j < grid[0].size(); ++j) {
                if (grid[i][j] == '1') {
                    dfs(grid, i, j);
                    count++;
                }
            }
        }
        return count;
    }
};

Question:
Leetcode 10: Regular Expression Matching
Implement regular expression matching with support for '.' and '*'.
Solution:
def isMatch(s, p):
    if not p:
        return not s
    first_match = bool(s) and p[0] in {s[0], '.'}
    if len(p) >= 2 and p[1] == '*':
        return isMatch(s, p[2:]) or (first_match and isMatch(s[1:], p))
    else:
        return first_match and isMatch(s[1:], p[1:])

Question:
Leetcode 84: Largest Rectangle in Histogram
Given an array of integers heights representing the histogram's bar height where the width of each bar is 1, return the area of the largest rectangle in the histogram.
Solution:
class Solution {
public:
    int largestRectangleArea(vector<int>& heights) {
        stack<int> st;
        heights.push_back(0);
        int maxArea = 0;
        for (int i = 0; i < heights.size(); ++i) {
            while (!st.empty() && heights[i] < heights[st.top()]) {
                int h = heights[st.top()]; st.pop();
                int w = st.empty() ? i : i - st.top() - 1;
                maxArea = max(maxArea, h * w);
            }
            st.push(i);
        }
        return maxArea;
    }
};

