import os
from hw_grading_system.main import DATA_PATH, SAVE_PATH

if not os.path.isdir(DATA_PATH):
    print(" >> Created data/ directory for saving score sheet")
    os.mkdir(DATA_PATH)

if not os.path.isdir(SAVE_PATH):
    print(" >> Created result/ directory for saving score sheet")
    os.mkdir(SAVE_PATH)