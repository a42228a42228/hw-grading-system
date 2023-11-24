import subprocess
import os
import time
import sys
import csv
from data import Database, FileLoader
from tester import Tester
from user_interface import UI, EXIT_KEY

DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),"..")) + "/data/"
SAVE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),"..")) + "/result/"
SCORE_SHEET_PAHT = SAVE_PATH + "score_sheet.csv"

def compile_file(file_loader):
    if file_loader.file_type != "c":
        print(" >> This file can't compile. Please check the file type")
        input(" >> Press 'Enter' go back to main menu")
        return

    output_file = file_loader.file_path[:-2]
    # Prepare the command
    command = ["gcc", file_loader.file_path, "-o", output_file, "-lm"]

    # Compile file
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _, stderr = process.communicate()

    # Display result of compiling
    if process.returncode != 0:     # error
        print(" >> Failed to compile!\n")
        print(f"### Error message ###\n{stderr.decode()}")
    else:
        print(" >> Compiled successfully")
        file_loader.executable_file_path = output_file
    input(" >> Press 'Enter' go back to main menu")

def test(file_loader, tester, ui, idx, total_files_num):
    while True:
        # display choose homework UI
        ui.display_text("test_display", **{"filename": file_loader.filename, "student_id": file_loader.student_id, "file_type": file_loader.file_type,  "idx": idx + 1, "total_files_num": total_files_num})

        # get test version
        test_input = ui.get_input("test_input")
        if test_input == "back":
            break
        if test_input == "wrong input":
            input(" >> Please input valid number. Press 'Enter' go back to test menu")
            continue

        # load test case
        test_case = tester.load_test_case(test_input)

        while True:
            # get test type
            test_type = ui.get_input("test_type_input")
            if test_type == "wrong input":
                input(" >> Please input valid number. Press 'Enter' go back to test menu")
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
        input(" >> Press 'Enter' go back to test menu")

def display_source_code(file_loader):
    try:
        with open(file_loader.file_path, 'r', encoding="utf-8") as f:
            source_code = f.read()
            print("\n==================  Source code   ==================\n")
            print(source_code)
            print("\n==================  End of source code   ==================\n")
    except:
        print(" >> Could not display source code")
    input("Press 'Enter' go back to main menu")

def display_test_result(file_loader):
    test_result = file_loader.test_result
    if test_result != None:
        print("\n==================  Test result   ==================\n")
        print(test_result)
        print("\n==================  End of test result   ==================\n")
    else:
        print(" >> There's no test result")
    input("Press 'Enter' go back to main menu")

def record_score(file_loader, score_sheet_path):
    # aviod wrong input
    score = input(" >> Please enter score (or just press 'Enter' go back to main menu): ")
    if score == "":
        file_loader.score = None
        return
    else:
        file_loader.score = score
    
    
    with open(score_sheet_path, "r", encoding="utf-8") as f:
        next(f)
        reader = csv.DictReader(f)
        content = [row for row in reader]
    
    # update score
    for row in content:
        # check if the score of filename already exist or not
        if file_loader.filename == row["Filename"] and file_loader.student_id == row["Student_id"]:
            row["Score"] = file_loader.score
            with open(score_sheet_path, "a", encoding="utf-8") as f:
                next(f)
                writer = csv.writer(f)
                writer.write(reader)
            break

    
    with open(score_sheet_path, "a", encoding="utf-8") as f:
        writer = csv.writer(f)







        # the score of filename not exist
        writer.writerow([file_loader.filename, file_loader.student_id, score])
        print(" >> Score recorded !")
    input("Press 'Enter' go back to main menu")

def run(process, kwargs):
    process(**kwargs)

def main():
    print("\n >> Welcome to homework grading system!")
    TA_name = ""
    TA_student_id = ""
    # get name and student for record score
    while True:
        if TA_name == "":
            TA_name = input(" >> Please Enter your name: ")
            # print(" >> Please Enter you name")
            continue
        if TA_student_id == "":
            TA_student_id = input(" >> Please Enter your student ID: ")
            continue
        if TA_name != "" and TA_student_id != "":
            break

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
    # set up for UI
    total_files_num = len(database)
    idx = 0

    # process functions
    process_func_dict = dict(
        compile = compile_file,
        test = test,
        display_test_result = display_test_result,
        display_source_code = display_source_code,
        record_score = record_score,
    )

    # process args
    process_args_dict = dict(
        compile = {
            "file_loader": file_loader, 
        },
        test = {
            "file_loader": file_loader, 
            "tester": tester,
            "ui": ui,
            "idx": idx,
            "total_files_num": total_files_num,
        },
        display_test_result = {
            "file_loader": file_loader, 
        },
        display_source_code = {
            "file_loader": file_loader, 
        },
        record_score = {
            "file_loader": file_loader,
            "score_sheet_path": SCORE_SHEET_PAHT,
        },
    )

    while idx < total_files_num:
        file_loader.load_file(database[idx]["file_path"], database[idx]["student_id"])
        while True:
            # display choosing mode UI
            ui.display_text("mode_display", **{"filename": file_loader.filename, "file_type": file_loader.file_type, "student_id": file_loader.student_id, "idx": idx + 1, "total_files_num": total_files_num})

            # control main menu
            user_input = ui.get_input("mode_input")
            if user_input == "next_file" :
                idx += 1
                break
            if user_input == "pre_file" :
                idx -= 1
                break
            if user_input == "wrong input":
                input(" >> Please input valid number. Press 'Enter' go back to main menu")
                continue
            if user_input == "exit":
                print("\n !!! Warning: Make sure you score all of the file !!! In this version you can't restart to score files !!! \n ")
                exit_check = input(" >> Do you really want to exit? yes(y) / no(n): ")
                if exit_check == 'y':
                    print(" >> Exit Successfully")
                    exit()
                elif exit_check == 'n':
                    continue
                else:
                    input(" >> Please input valid number. Press 'Enter' go back to main menu")
                    continue

            
            # run the process which user choose
            process_func = process_func_dict[user_input]
            progess_args = process_args_dict[user_input]
            run(process_func, progess_args)
        
        # control pre/next file
        if idx == total_files_num:
            print(" >> This is the last file. ")
            print(" >> You could Press 'Esc' to exit or press any other key to stay")
            exit_check = sys.stdin.readline().strip()
            if exit_check == EXIT_KEY:
                print(" >> Exit Successfully")
                exit()
            else:
                idx = total_files_num - 1
                continue
        elif idx < 0:
            print(" >> This is the first file. You can't go previous file")
            input(" >> Press 'Enter' go back to main menu")
            idx = 0

if __name__ == '__main__':
    main()