
nums = [5,4,3,6,7]
target = 9
hasht = {}
class Solution(object):
    def two_sum(nums, target):
        counter = len
        for i in nums:
            for j in nums:
                if i + j == target:
                    return print("[{},{}]".format(nums[i],nums[j]))
                else:
                    pass
    two_sum(nums, target)