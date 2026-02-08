def binary_search(arr, target):
    low = 0
    high = len(arr) - 1

    while low <= high:
        # 找到中间位置的索引
        mid = (low + high) // 2
        guess = arr[mid]

        # 找到了！
        if guess == target:
            return mid

        # 猜大了，往左找
        if guess > target:
            high = mid - 1

        # 猜小了，往右找
        else:
            low = mid + 1

    # 如果没找到，返回 None
    return None


# 测试一下
my_list = [1, 3, 5, 7, 9, 11, 13, 15]
target_value = 7

result = binary_search(my_list, target_value)

if result is not None:
    print(f"找到了！元素 {target_value} 在索引 {result} 的位置。")
else:
    print("很遗憾，它不在这里。")