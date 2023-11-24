import os
import subprocess
import tarfile
import zipfile

FILE_SUBMISSION_DIRECTORY = "assignsubmission_file"
compression_file = ['.tar', '.gz', '.tgz', '.tar.gz', '.tar.tgz', '.bz2', '.tar.bz2', '.zip', '.rar', '.lha']

class Database():
    def __init__(self, dir_path):
        self.dir_path = dir_path
        self.data = self._collect_files(self.dir_path)

    def __getitem__(self, idx):
        return self.data[idx]

    def __len__(self):
        return len(self.data)

    def _collect_files(self, dir_path):
        # Check if directory exists
        if not os.path.isdir(dir_path):
            print(f"No such directory: {dir_path}")
            return
        
        # decompress files
        self._decompression_files(dir_path)

        # get all submission file directory path
        dirs = [dir_path + "/" + dir for dir in os.listdir(dir_path) if dir.endswith(FILE_SUBMISSION_DIRECTORY)]
        dirs.sort()

        # collate files from each submission file directory
        data = []
        for dir in dirs:
            # get student ID from directory name
            student_id = dir.split("/")[-1].split(" ")[0]
            file_path_list = self._explore_files(dir)
            # refine data in directory
            dir_data = [{"student_id": student_id, "file_path": file_path} for file_path in file_path_list]
            data += dir_data
        return data

    def _explore_files(self, dir):
        file_path_list = []
        for root, _, files in os.walk(dir):
            for file in files:
                file_path = os.path.join(root, file)
                file_path_list.append(file_path)
        return file_path_list

    def _decompression_files(self, dir):
        for root, _, files in os.walk(dir):
            for file in files:
                file_path = os.path.join(root, file)
                file_type = os.path.splitext(file_path)[1]
                # check if file is compression file
                if file_type in compression_file:
                    self._decompression(file_path)

    def _decompression(self, file_path):
        file_type = os.path.splitext(file_path)[1]
        dir_path = os.path.dirname(file_path)
        if file_type in ['.tar', '.gz', '.tgz', '.tar.gz', '.tar.tgz']:
            with tarfile.open(file_path, 'r:gz') as tar:
                tar.extractall(dir_path)
        elif file_type in ['.bz2', '.tar.bz2']:
            with tarfile.open(file_path, 'r:bz2') as tar:
                tar.extractall(dir_path)
        elif file_type == '.zip':
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(dir_path)
        elif file_type == '.rar':
            subprocess.run(['unrar', 'x', file_path])
        elif file_type == '.lha':
            subprocess.run(['lha', 'e', file_path])
        else:
            raise ValueError(f'Unsupported file type: {file_type}')

class FileLoader():    
    def load_file(self, file_path, student_id):
        self.file_path = file_path
        self.student_id = student_id
        self.filename = os.path.basename(file_path)
        self.file_type = self.split_file_type(self.filename)
        self.executable_file_path = None
        self.score = None
        self.test_result = None

    def isTestable(self):
        if self.executable_file_path == None:
            return False
        else:
            return True
    
    def split_file_type(self, filename):
        if "." not in filename:
            return "out"
        else:
            return filename.split(".")[-1]