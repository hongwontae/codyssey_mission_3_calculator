def mac(input_data, filter_data):
    score = 0

    # i -> 0이 고정일 떄 j는 0,1,2로 변함
    # 즉, i는 행을 이미하고 j는 열을 의미함
    for i in range(3):
        for j in range(3):
            score += input_data[i][j] * filter_data[i][j]

    return score


input_data = [
    [0, 1, 0],
    [1, 1, 1],
    [0, 1, 0]
]

cross_filter = [
    [0, 1, 0],
    [1, 1, 1],
    [0, 1, 0]
]

print(mac(input_data, cross_filter))