import subprocess
import csv
import os
import time
from data import Database, FileLoader
from tester import Tester
from user_interface import UI

DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),"..")) + "/data/"
SAVE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),"..")) + "/result/"
SCORE_SHEET_PAHT = SAVE_PATH + "score_sheet.csv"

PROCESS_FUNC_DICT = dict(
    compile = compile_file,
    test = test,
    display_test_result = display_test_result,
    display_source_code = display_source_code,
    record_score = record_score,
)

def compile_file(file_loader):
    if file_loader.file_type != "c":
        print(" -> This file can't compile. Please check the file type")
        input(" -> Press 'Enter' go back to main menu")
        return

    output_file = file_loader.file_path[:-2]
    # Prepare the command
    command = ["gcc", file_loader.file_path, "-o", output_file, "-lm"]

    # Compile file
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _, stderr = process.communicate()

    # Display result of compiling
    if process.returncode != 0:     # error
        print(" -> Failed to compile!\n")
        print(f"### Error message ###\n{stderr.decode()}")
    else:
        print(" -> Compiled successfully")
        file_loader.executable_file_path = output_file
    input(" -> Press 'Enter' go back to main menu")

def test(file_loader, tester, ui):
    while True:
        # display choose homework UI
        ui.display_text("test_display", **{"filename": file_loader.filename, "student_id": file_loader.student_id})

        # get test version
        test_input = ui.get_input("test_input")
        if test_input == "back":
            break
        if test_input == "wrong input":
            input(" -> Please input valid number. Press 'Enter' go back to test menu")
            continue

        # load test case
        test_case = tester.load_test_case(test_input)

        while True:
            # get test type
            test_type = ui.get_input("test_type_input")
            if test_type == "wrong input":
                input(" -> Please input valid number. Press 'Enter' go back to test menu")
                continue
            # test
            if test_type == "auto_test":
                tester.run_auto_test(file_loader, test_case)
                tester.show_answer(test_input)
                break
            elif test_type == "manual_test":
                break
            elif test_type == "back":
                break
    input(" -> Press 'Enter' go back to main menu")

def display_source_code(file_loader):
    try:
        with open(file_loader.file_path, 'r', encoding="utf-8") as f:
            source_code = f.read()
            print("\n==================  Source code   ==================\n")
            print(source_code)
            print("\n==================  End of source code   ==================\n")
    except:
        print(" -> Could not display source code")
    input("Press 'Enter' go back to main menu")

def display_test_result(file_loader):
    test_result = file_loader.test_result
    if test_result != None:
        print("\n==================  Test result   ==================\n")
        print(test_result)
        print("\n==================  End of test result   ==================\n")
    else:
        print(" -> There's no test result")
    input("Press 'Enter' go back to main menu")

def record_score(file_loader, score_sheet_path):
    # aviod wrong input
    score = input(" -> Please enter score (or just press 'Enter' go back to main menu): ")
    if score == "":
        file_loader.score = None
        return
    else:
        file_loader.score = score
    
    with open(score_sheet_path, "a", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([file_loader.filename, file_loader.student_id, score])
        print(" -> Score recorded !")
    input("Press 'Enter' go back to main menu")

def run(process, kwargs):
    process(**kwargs)

def main():
    # get name for record score
    TA_name = input("Please Enter your name: ")
    TA_student_id = input("Please Enter your student ID: ")
    date = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())

    # record TA name and student id into score sheet
    with open(SCORE_SHEET_PAHT, "a", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["TA name", TA_name, "TA student ID", TA_student_id, "Date", date])
        writer.writerow([ "Filename", "Student ID", "Score"])

    # set up
    database = Database(DATA_PATH)
    file_loader = FileLoader()
    ui = UI()
    tester = Tester() 
    process_args_dict = dict(
        compile = {
            "file_loader": file_loader, 
        },
        test = {
            "file_loader": file_loader, 
            "tester": tester,
            "ui": ui,
        },
        display_test_result = {
            "file_loader": file_loader, 
        },
        display_source_code = {
            "file_loader": file_loader, 
        },
        record_score = {
            "file_loader": file_loader,
            "score_sheet_path": score_sheet_path,
        },
    )

    # go through every files in database
    for file in database:
        for file_path in file['homework_files']:
            # load file
            file_loader.load_file(file_path, file['student_id'])

            while True:
                # display choosing mode UI
                ui.display_text("mode_display", **{"filename": file_loader.filename, "file_type": file_loader.file_type, "student_id": file_loader.student_id})

                # get user input
                user_input = ui.get_input("mode_input")
                if user_input == "next_file" :
                    input(" -> Press 'Enter' to goto next file")
                    break
                if user_input == "wrong input":
                    input(" -> Please input valid number. Press 'Enter' go back to main menu")
                    continue
                if user_input == "exit":
                    print("\n !!! Warning: Make sure you score all of the file !!! In this version you can't restart to score files !!! \n ")
                    exit_check = input(" -> Do you really want to exit? 1) yes, 2) no: ")
                    if exit_check == '1':
                        print(" -> Exit Successfully")
                        exit()
                    else:
                        continue
                
                # run the process which user choose
                process = PROCESS_FUNC_DICT[user_input]
                progess_args = process_args_dict[user_input]
                run(process, progess_args)

if __name__ == '__main__':
    main()