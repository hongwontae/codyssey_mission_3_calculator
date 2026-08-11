
CROSS_FILTER = [
    [0, 1, 0],
    [1, 1, 1],
    [0, 1, 0]
]

X_FILTER = [
    [1, 0, 1],
    [0, 1, 0],
    [1, 0, 1]
]


def mac(input_data, filter_data):
    score = 0

    for i in range(3):
        for j in range(3):
            score += input_data[i][j] * filter_data[i][j]

    return score

def input_matrix():
    matrix = []

    print("3개의 숫자를 공백으로 구분해서 입력하세요.")

    for i in range(3):
        while True:
            try:
                row = list(map(int, input(f"{i + 1}번째 행: ").split()))

                # 숫자가 정확히 3개인지 확인
                if len(row) != 3:
                    print("숫자 3개를 입력해주세요.")
                    continue

                # 0 또는 1인지 확인 [0, 1, 0]
                if any(value not in (0, 1) for value in row):
                    print("0 또는 1만 입력해주세요.")
                    continue

                matrix.append(row)
                break

            except ValueError:
                print("숫자만 입력해주세요.")

    return matrix

# 판정
def classify(cross_score, x_score):
    # 두 점수가 거의 같으면 UNDECIDED
    if abs(cross_score - x_score) <= 1e-9:
        return "UNDECIDED"

    if cross_score > x_score:
        return "Cross"

    return "X"

def run_user_mode():

    print()
    print("#" + "-" * 30)
    print("# [1] 패턴 입력")
    print("#" + "-" * 30)

    input_data = input_matrix()

    print()
    print("#" + "-" * 30)
    print("# [2] MAC 결과")
    print("#" + "-" * 30)

    # Cross 필터와 MAC
    cross_score = mac(input_data, CROSS_FILTER)

    # X 필터와 MAC
    x_score = mac(input_data, X_FILTER)

    # 판정
    result = classify(cross_score, x_score)

    print(f"Cross 점수: {cross_score}")
    print(f"X 점수: {x_score}")
    print(f"판정: {result}")

def main():

    try :
        while True:
            print()
            print("=== Mini NPU Simulator ===")
            print()

            print("[모드 선택]")
            print("1. 사용자 입력 (3x3)")
            print("2. data.json 분석")
            print("0. 종료")

            print()
            choice = input("선택: ")

            if choice == "1":
                run_user_mode()

            elif choice == "2":
                print("모드 2는 아직 구현하지 않았습니다.")

            elif choice == "0":
                print("프로그램을 종료합니다.")
                break

            else:
                print("잘못된 선택입니다.")
    except (KeyboardInterrupt, EOFError) :
        print("프로그램을 안전하게 종료합니다.") 


if __name__ == "__main__":
    main()