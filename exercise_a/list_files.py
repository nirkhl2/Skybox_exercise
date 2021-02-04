import os
import sys
import socket


# Verify the user arguments to the script are valid (input folder must found in the os, and of type directory)
def verify_user_input(args):
    script_syntax = "Try running again using script syntax: 'python list_files.py <full_path_to_scan>'"
    if len(args) == 2:
        if not (os.path.exists(args[1])):
            print("Failure! The input path '{}' does NOT exist at the current host '{}'\n{}".format(args[1], socket.gethostname(), script_syntax))
            exit(1)
        if not (os.path.isdir(args[1])):
            print("Failure! The input path '{}' is NOT a directory in the current host '{}'\n{}".format(args[1], socket.gethostname(), script_syntax))
            exit(1)
    if len(args) < 2:
        print("Failure! Missing directory input argument to script!\n" + script_syntax)
        exit(1)
    if len(args) > 3:
        print("Failure! Too many arguments sent to script!\n" + script_syntax)
        exit(1)


# This method is receiving a full path and listing all files and directories including subfolders using recursive calls - print out the results
def list_files(path):
    indent = " " * 3
    directory_level = path.count(os.sep)  # count the file separators in order to know the current level of folder - for clearer print of result tree
    print("{}{}{}".format(indent * directory_level, os.path.basename(path), os.sep))  # print directory with the relevant directory level
    for entry in os.listdir(path):
        entry_path = os.path.join(path, entry)
        directory_level = entry_path.count(os.sep)
        if os.path.isfile(entry_path):
            print("{}{}".format(indent * directory_level, entry))  # print file with the relevant directory level
        if os.path.isdir(entry_path):
            list_files(entry_path)  # The recursive call


if __name__ == '__main__':
    verify_user_input(sys.argv)
    list_files(path=sys.argv[1])
