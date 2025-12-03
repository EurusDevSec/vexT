

def modes_simple(nums):
    # Trả về danh sách các phần tử xuất hiện nhiều nhất (có thể nhiều hơn 1)
    if not nums:
        return []

    # Tạo danh sách các phần tử duy nhất giữ nguyên thứ tự xuất hiện
    uniques = []
    for x in nums:
        if x not in uniques:
            uniques.append(x)

    # Đếm tần suất cho mỗi phần tử duy nhất 
    counts = []
    for u in uniques:
        c = 0
        for v in nums:
            if v == u:
                c += 1
        counts.append(c)

    # Tìm tần suất lớn nhất
    max_count = counts[0]
    for c in counts:
        if c > max_count:
            max_count = c

    # Gom các phần tử có tần suất bằng tần suất lớn nhất
    result = []
    for u, c in zip(uniques, counts):
        if c == max_count:
            result.append(u)

    return result


if __name__ == '__main__':
    tests = [
        [1, 2, 2, 3, 3, 3, 4],
        [1, 2, 2, 3, 3],
        [],
        [5, 5, 6, 6, 7],
    ]

    for t in tests:
        print('Input:', t)
        print('Mode(s):', modes_simple(t))
        print('---')