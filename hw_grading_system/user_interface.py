MODE_UI_DISPLAY_TEXT = """
=====================================================
                    MAIN    MENU
=====================================================
         ---   {file_idx}  /  {total_files_num}   ---
- FILENAME: {filename} / FILETYPE: .{file_type}
- STUDENT ID: {student_id} 
- MODE:
    1) Compile file
    2) Test file
    3) Display test result
    4) Display source file
    5) Record score
=====================================================
<- pre file (p)        exit(0)       (n) next file ->
"""

TEST_UI_DISPLAY_TEXT = """
=====================================================
                    TEST    MENU
=====================================================
         ---   {file_idx}  /  {total_files_num}   ---
- FILENAME: {filename} / FILETYPE: .{file_type}
- STUDENT ID: {student_id} 
- Avaliable homework name:
    1) [homework 01] 03rd class
    2) [homework 02] 03rd class
    3) [homework] 04th class
    4) [Assignment] 06th class (Bisection Method)
    5) [Assignment] 06th class (Newton Method)
=====================================================
<- back to main menu (b)
"""

DISPLAY_TEXT_DICT = dict(
    mode_display = MODE_UI_DISPLAY_TEXT,
    test_display = TEST_UI_DISPLAY_TEXT,
)

MODE_UI_INPUT_TEXT = "\n -> Please input the number of MODE: "
TEST_UI_INPUT_TEXT = "\n -> Please input the number of homework name: "
TEST_TYPE_INPUT_TEXT = "\n -> Please choose  1) Auto-test   2) Manual-test  3) back to test menu :"
INPUT_TEXT_DICT = dict(
    mode_input = MODE_UI_INPUT_TEXT,
    test_input = TEST_UI_INPUT_TEXT,
    test_type_input = TEST_TYPE_INPUT_TEXT,
)

MODE_CHOOSE_DICT = dict(
    [
        # mode for user to choose
        ("0", "exit"),
        ("1", "compile"),
        ("2", "test"),
        ("3", "display_test_result"),
        ("4", "display_source_code"),
        ("5", "record_score"),
        ("n", "next_file"),
        ("p", "pre_file"),
    ]
)

TESTER_CHOOSE_DICT = dict(
    [
        # avaliable teser for user to choose
        ("b", "back"),
        ("1", "hw-3-1"),
        ("2", "hw-3-2"),
        ("3", "hw-4"),
        ("4", "hw-6-1"),
        ("5", "hw-6-2"),
    ]
)

TEST_TYPE_CHOOSE_DICT = dict(
    [
        ("1", "auto_test"),
        ("2", "manual_test"),
        ("3", "back")
    ]
)

CHOOSE_DICT = dict(
    mode_input = MODE_CHOOSE_DICT,
    test_input = TESTER_CHOOSE_DICT,
    test_type_input = TEST_TYPE_CHOOSE_DICT,
)

class UI():
    def get_input(self, input_text_type) -> str:
        choose = input(INPUT_TEXT_DICT[input_text_type])
        if choose not in CHOOSE_DICT[input_text_type]:
            return "wrong input"
        return CHOOSE_DICT[input_text_type][choose]

    def display_text(self, display_text_type, **kwargs):
            print(DISPLAY_TEXT_DICT[display_text_type].format(**kwargs))