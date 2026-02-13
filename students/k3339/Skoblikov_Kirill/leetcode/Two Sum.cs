public class Solution
{
    public int[] TwoSum(int[] nums, int target)
    {
        int[] result = [];
        for (int i = 0; i < nums.Length-1; i++)
        {
            for (int g = i+1; g < nums.Length; g++)
            {
                if (nums[i] + nums[g] == target)
                {
                    result = [i, g];
                    return result;
                }
            }
        }
        return result;
    }
}