from subprocess import check_output
import os.path
import glob


def main():
    if os.path.exists('.woosh'):
        venv_path = glob.glob('**/activate', recursive=True)
        if venv_path:
            print("Activating venv")
            os.system('/bin/bash --rcfile ' + venv_path[0])
        else:
            os.system('python -m venv venv ')
        print("Created venv")
    else:
        print("Creating woosh..")
        with open('.woosh', 'x') as f:
            f.write('Create a new text file!')
