import json
import time

def run_json_mode():
    try :
        with open("data.json", "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        print("data.json 파일을 찾을 수 없습니다.")
        return

    except json.JSONDecodeError:
        print("data.json의 JSON 형식이 올바르지 않습니다.")
        return

    if not isinstance(data, dict) :
        print("FAIL : data.json의 최상위 구조가 올바르지 않습니다.")
        return

    if "patterns" not in data:
        print("FAIL: data.json에 patterns가 없습니다.")
        return

    if "filters" not in data:
        print("FAIL: data.json에 filters가 없습니다.")
        return

    patterns = data["patterns"]
    filters = data["filters"]

    if not isinstance(patterns, dict) :
        print("FAIL: patterns가 올바른 형식이 아닙니다.")
        return 
    
    if not isinstance(filters, dict) :
        print("FAIL: filters가 올바른 형식이 아닙니다.")
        return

    total = 0
    passed = 0
    failed = 0
    fail_cases = []

    for pattern_name, pattern in patterns.items():

        if not isinstance(pattern, dict):
            print("결과: FAIL")
            print("사유: 패턴 데이터 형식이 올바르지 않습니다.")
            failed += 1
            total += 1
            fail_cases.append((pattern_name, "사유: 패턴 데이터 형식이 올바르지 않습니다."))
            continue

        print()
        print("#" + "-" * 30)
        print(f"# [{pattern_name}]")
        print("#" + "-" * 30)

        if "input" not in pattern:
            print("결과: FAIL")
            print("사유: input이 없습니다.")
            failed += 1
            total += 1
            fail_cases.append((pattern_name, "사유: input이 없습니다."))
            continue

        if "expected" not in pattern:
            print("결과: FAIL")
            print("사유: expected가 없습니다.")
            failed += 1
            total += 1
            fail_cases.append((pattern_name, "사유: expected가 없습니다."))
            continue

        input_data = pattern["input"]
        expected = pattern["expected"]

        if expected not in ("+", "x", "X", "UNDECIDED"):
            print("결과: FAIL")
            print("사유: expected 값이 올바르지 않습니다.")
            failed += 1
            total += 1
            fail_cases.append((pattern_name,"사유: expected 값이 올바르지 않습니다."))
            continue

        parts = pattern_name.split("_")

        if len(parts) != 3 or parts[0] != "size":
            print("결과: FAIL")
            print("사유: 패턴 이름 형식이 올바르지 않습니다.")
            failed += 1
            total += 1
            fail_cases.append((pattern_name, "사유: 패턴 이름 형식이 올바르지 않습니다."))
            continue

        try:
            size = int(parts[1])
        except ValueError:
            print("결과: FAIL")
            print("사유: 패턴 크기가 숫자가 아닙니다.")
            failed += 1
            total += 1
            fail_cases.append((pattern_name, "사유: 패턴 크기가 숫자가 아닙니다."))
            continue

        ## 여기부터 시작!
        if not validate_matrix(input_data, size):
            print("결과: FAIL")
            print("사유: 패턴 크기가 올바르지 않습니다.")
            failed += 1
            total += 1
            fail_cases.append((pattern_name, "사유: 패턴 크기가 올바르지 않습니다."))
            continue

        ## parts[:2] -> ["size", "n"]
        ## "_".join -> "size_n" -> filter의 키로 사용하겠다.
        size_key = "_".join(parts[:2])

        if size_key not in filters:
            print("결과: FAIL")
            print(f"사유: {size_key} 필터가 없습니다.")
            failed += 1
            total += 1
            fail_cases.append((pattern_name, f"사유: {size_key} 필터가 없습니다."))
            continue

        # {cross : [2차원배열], x : [2차원배열]}
        size_filter = filters[size_key]

        if not isinstance(size_filter, dict):
            print("결과: FAIL")
            print("사유: 필터 데이터 형식이 올바르지 않습니다.")
            failed += 1
            total += 1
            fail_cases.append((pattern_name, "사유: 필터 데이터 형식이 올바르지 않습니다."))
            continue

        if "cross" not in size_filter:
            print("결과: FAIL")
            print("사유: Cross 필터가 없습니다.")
            failed += 1
            total += 1
            fail_cases.append((pattern_name, "사유: Cross 필터가 없습니다."))
            continue

        if "x" not in size_filter:
            print("결과: FAIL")
            print("사유: X 필터가 없습니다.")
            failed += 1
            total += 1
            fail_cases.append((pattern_name, "사유: X 필터가 없습니다."))
            continue

        # filter 2차원 배열
        cross_filter = size_filter["cross"]
        x_filter = size_filter["x"]

        # -> pattern의 key로 filter를 찾았으니까 size 그대로 써도 ㄱㅊ
        if not validate_filter_matrix(cross_filter, size):
            print("결과: FAIL")
            print("사유: Cross 필터 크기가 올바르지 않습니다.")
            failed += 1
            total += 1
            fail_cases.append((pattern_name, "사유: Cross 필터 크기가 올바르지 않습니다."))
            continue

        if not validate_filter_matrix(x_filter, size):
            print("결과: FAIL")
            print("사유: X 필터 크기가 올바르지 않습니다.")
            failed += 1
            total += 1
            fail_cases.append((pattern_name, "사유: X 필터 크기가 올바르지 않습니다."))
            continue

        # MAC 점수
        cross_score = mac(input_data, cross_filter)
        x_score = mac(input_data, x_filter)

        result = classify(cross_score, x_score)

        # JSON의 expected 라벨을 프로그램 판정값으로 변환
        normalized_expected = normalize_expected(expected)

        print("Cross 점수:", cross_score)
        print("X 점수:", x_score)
        print("점수 차이:", abs(cross_score - x_score))
        print("판정:", result)
        print("정답:", normalized_expected)

        total += 1

        if result == normalized_expected:
            print("결과: PASS")
            passed += 1

        else:
            print("결과: FAIL")
            failed += 1

            reason = (f"판정 결과({result})와 " f"expected({normalized_expected})가 다릅니다.")
            fail_cases.append((pattern_name, reason))

    run_performance_analysis()


    print()
    print("#" + "-" * 30)
    print("# [4] 결과 요약")
    print("#" + "-" * 30)

    print(f"총 테스트: {total}개")
    print(f"통과: {passed}개")
    print(f"실패: {failed}개")

    if fail_cases:
        print()
        print("실패 케이스:")

        for pattern_name, reason in fail_cases:
            print(f"- {pattern_name}: {reason}")

def mac(input_data, filter_data):
    score = 0

    size = len(input_data)

    for i in range(size):
        for j in range(size):
            score += input_data[i][j] * filter_data[i][j]

    return score

def benchmark_mac(input_data, filter_data):
    repeat = 10

    start = time.perf_counter()

    for _ in range(repeat):
        mac(input_data, filter_data)

    end = time.perf_counter()

    average_time = (end - start) / repeat

    return average_time * 1000

def generate_benchmark_matrix(size):
    matrix = []

    for i in range(size):
        row = []

        for j in range(size):
            row.append(1.0)

        matrix.append(row)

    return matrix

def validate_matrix(matrix, expected_size):
    if not isinstance(matrix, list):
        return False

    if len(matrix) != expected_size:
        return False

    for row in matrix:
        if not isinstance(row, list):
            return False

        if len(row) != expected_size:
            return False

        for value in row:
            if value not in (0, 1):
                return False

    return True

def validate_filter_matrix(matrix, expected_size):
    if not isinstance(matrix, list):
        return False

    if len(matrix) != expected_size:
        return False

    for row in matrix:
        if not isinstance(row, list):
            return False

        if len(row) != expected_size:
            return False

        for value in row:
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                return False

    return True

def run_performance_analysis():

    print()
    print("#" + "-" * 30)
    print("# [3] 성능 분석")
    print("#" + "-" * 30)

    print("크기\t평균 시간(ms)\t연산 횟수")

    for size in (3, 5, 13, 25):

        pattern = generate_benchmark_matrix(size)
        filter_data = generate_benchmark_matrix(size)

        average_time = benchmark_mac(
            pattern,
            filter_data
        )

        operation_count = size * size

        print(
            f"{size}x{size}\t"
            f"{average_time:.3f}\t\t"
            f"{operation_count}"
        )

def input_matrix_3x3():
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

def classify(cross_score, x_score):
    if abs(cross_score - x_score) < 1e-9:
        return "UNDECIDED"

    if cross_score > x_score:
        return "Cross"

    return "X"

def classify_ab(a_score, b_score):
    if abs(a_score - b_score) < 1e-9:
        return "UNDECIDED"

    if a_score > b_score:
        return "A"

    return "B"

def normalize_expected(expected):
    if expected == "+":
        return "Cross"

    if expected.lower() == "x":
        return "X"

    return "UNDECIDED"

def run_user_mode():

    print()
    print("#" + "-" * 30)
    print("# [1] 필터 A 입력")
    print("#" + "-" * 30)

    filter_a = input_matrix_3x3()

    print()
    print("#" + "-" * 30)
    print("# [2] 필터 B 입력")
    print("#" + "-" * 30)

    filter_b = input_matrix_3x3()

    print()
    print("#" + "-" * 30)
    print("# [3] 패턴 입력")
    print("#" + "-" * 30)

    input_data = input_matrix_3x3()

    print()
    print("#" + "-" * 30)
    print("# [4] MAC 결과")
    print("#" + "-" * 30)

    # MAC 점수
    a_score = mac(input_data, filter_a)
    b_score = mac(input_data, filter_b)

    # 성능 측정
    a_time = benchmark_mac(input_data, filter_a)
    b_time = benchmark_mac(input_data, filter_b)

    # 판정
    result = classify_ab(a_score, b_score)

    print(f"A 점수: {a_score}")
    print(f"B 점수: {b_score}")
    print(f"A 평균 연산 시간(10회): {a_time:.3f} ms")
    print(f"B 평균 연산 시간(10회): {b_time:.3f} ms")
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
                run_json_mode()

            elif choice == "0":
                print("프로그램을 종료합니다.")
                break

            else:
                print("잘못된 선택입니다.")
    except (KeyboardInterrupt, EOFError) :
        print("프로그램을 안전하게 종료합니다.") 


if __name__ == "__main__":
    main()