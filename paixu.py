def pd(x, y, li):
    # print(li)
    for i in li:
        # print(x[i], y[i])
        if x[i] > y[i]:
            return 1
        elif x[i] < y[i]:
            return 0
    return 1


def upsort(arr, left, right, li):
    if left >= right:
        return arr
    init_left = left
    init_right = right
    key = arr[left]
    while left < right:
        while left < right and pd(arr[right], key, li):
            right -= 1
        arr[left] = arr[right]
        while left < right and pd(key, arr[left], li):
            left += 1
        arr[right] = arr[left]
    arr[left] = key
    upsort(arr, init_left, left-1, li)
    upsort(arr, left+1, init_right, li)
    return arr


def downsort(arr, left, right, li):
    if left >= right:
        return arr

    init_left = left
    init_right = right
    key = arr[right]

    while left < right:
        while left < right and pd(arr[left], key, li):
            left += 1
        arr[right] = arr[left]
        while left < right and pd(key, arr[right], li):
            right -= 1
        arr[left] = arr[right]
    arr[right] = key
    downsort(arr, init_left, left - 1, li)
    downsort(arr, right + 1, init_right, li)
    return arr


if __name__ == '__main__':
    a = [[1, 0, 3], [3, 1, 2], [2, 1, 5]]
    print(a)
    b = downsort(a, 0, len(a) - 1, [1, 0, 2])
    print(a)
    print(b)
