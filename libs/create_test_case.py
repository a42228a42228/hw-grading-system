import random
import os

def create_testcase():
    # test case: multiple 2 random 2D-arrays
    # set m, k, n
    m = random.randint(1, 5)
    k = random.randint(1, 5)
    n = random.randint(1, 5)
    # set M
    M = [random.uniform(0.0, 10.0) for i in range(m * k)]
    # set N
    N = [random.uniform(0.0, 10.0) for i in range(k * n)]

    # output test case file
    all_data = [m, k, n] + M + N
    return all_data

def save_testcase(all_data, test_case_name):
    current_dir = os.path.dirname(__file__)
    with open(current_dir + '/test_case/' + test_case_name + '.txt', 'w') as f:
        for data in all_data:
            if isinstance(data, float):
                data = round(data, 2)
            f.write(str(data) + '\n')
    return all_data

def main():
    data = create_testcase()
    save_testcase(data, "test_case_1")

if __name__ == '__main__':
  main() 

