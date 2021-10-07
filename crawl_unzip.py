import os,glob,tarfile, pathlib

def untar(path):

    for path, directories, files in os.walk(path):
        for f in files:
            if f.endswith(".tgz"):
                tar = tarfile.open(os.path.join(path,f), 'r:gz')
                tar.extractall(path=path)
                tar.close()

def main():
    path = r"C:\Users\Gerun\PycharmProjects\291Internship\script_grader\downloaded_answers"
    with open(r"C:\Users\Gerun\PycharmProjects\291Internship\script_grader\downloaded_answers\Zhengdao Yu_15629217_assignsubmission_file_\3.sql",'r') as f:
        for row in f:
            print(row)
main()