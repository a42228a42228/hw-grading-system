import os
import subprocess

TEST_CASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),"..")) + "/test_case/"

HOMEWORK_NAME_DICT = dict(
    [
        # avaliable teser for user to choose
        ("hw-3-1", "test_case_hw-3-1"),
        ("hw-3-2", "test_case_hw-3-2"),
        ("hw-4", "test_case_hw-4"),
        ("hw-6-1", "test_case_hw-6-1"),
        ("hw-6-2", "test_case_hw-6-2"),
    ]
)

class Tester():
    def load_test_case(self, homework_name):
        test_case_name = HOMEWORK_NAME_DICT[homework_name]
        test_case_path = TEST_CASE_DIR + test_case_name + "/test_case.txt"
        try:
            with open(test_case_path , "r", encoding="utf-8") as f:
                test_case = f.read()
            print(" >> Test case load successfully")
            return test_case
        except:
            print(" >> Test case not exsist. Please choose Manual-test")
            return None

    def run_auto_test(self, file, test_case):
        if not file.isTestable():
            print(" >> File is not executable. Please go back to main menu and choose 'Compile file' or 'Go to next file'.")
            input(" >> Press 'Enter' to go back to test menu")
            return -1
        
        if test_case is None:
            print(" >> There is no test case. Auto test is not avaliable.")
            input(" >> Press 'Enter' to go back to test menu")
            return -1

        # run file
        command = [file.executable_file_path]
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # change test case to binary
        stdin = test_case.encode()
        stdout, stderr = process.communicate(stdin)

        # return result
        if process.returncode != 0:     # error
            print(" >> Failed to test!\n")
            print("\n==================   Error Message   ==================\n")
            result = stderr.decode()
        else:
            print("\n==================  Standard Output   ==================\n")
            result = stdout.decode()
        print(result)
        file.test_result = result
        print("\n==================  End of Output   ==================\n")
    
    def show_answer(self, homework_name):
        test_case_name = HOMEWORK_NAME_DICT[homework_name]
        answer_path = TEST_CASE_DIR + test_case_name + "/answer.txt"        
        try:
            with open(answer_path , "r", encoding="utf-8") as f:
                test_case = f.read()
            print("==================     Answer       ==================")
            print(test_case)
        except:
            print(" >> Test answer not exsist")