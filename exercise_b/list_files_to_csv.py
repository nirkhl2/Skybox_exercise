import os
import sys
import socket
import hashlib
import csv


# This method is receiving a full path and listing all files including subfolders using recursive calls, return list of all files (files only)
def list_files(path):
    files = list()
    for entry in os.listdir(path):
        entry_path = os.path.join(path, entry)
        if os.path.isfile(entry_path):
            files.append(entry_path)
        if os.path.isdir(entry_path):
            files = files + list_files(entry_path)  # The recursive call

    return files


# This method is receiving a file and will encode the file content into MD5 using hashlib module
def encode_file_to_md5(file):
    file_as_byte = get_file_as_bytes(file)  # read the file content
    if file_as_byte is not None:
        file_md5_value = hashlib.md5(file_as_byte).hexdigest()  # Create the MD5 encode from the file content
    else:
        return None
    return file_md5_value


# This method will create the list data that will contain a dictionary per each file entry (will create the MD5 during and insert into the dictionary)
def create_data_per_file(files):
    list_files_data = list()
    index = 1
    for file_entry in files:
        entry_dict_data = dict()
        entry_dict_data['File Path'] = file_entry
        entry_dict_data['MD5'] = encode_file_to_md5(file_entry)
        entry_dict_data['Index'] = index
        index = index + 1
        list_files_data.append(entry_dict_data)

    return list_files_data


# This method will write the data into csv file using the list input from method 'create_data_per_file', used the csv module
def write_to_csv_file(files_data, path=sys.argv[1]):
    fields = ['Index', 'File Path', 'MD5']
    file_path = os.path.join(path, "files_data.csv")

    try:
        # writing to csv file
        csv_file = open(file_path, 'w')
        # creating a csv writer object
        writer = csv.DictWriter(csv_file, delimiter=',', lineterminator='\n', fieldnames=fields)

        # writing headers (field names)
        writer.writeheader()

        # writing data rows
        writer.writerows(files_data)
        csv_file.close()
    except IOError as e:
        print("Unable to create file on disk. '{}' content\nI/O error({}): {}".format(str(file_path), sys.exc_info()[0], str(e)))
    finally:
        verify_output_result_file(file_path)


# Method will read the file content and return the file content as bytes
def get_file_as_bytes(file):
    try:
        return open(file, 'rb').read()
    except IOError as e:
        print("Error occurred during attempt to read file '{}' content\nI/O error({}): {}".format(str(file.name), sys.exc_info()[0], str(e)))
        return None
    except Exception as e:  # handle other exceptions such as attribute errors
        print("Error occurred during attempt to read file '{}' content\nUnexpected error: {}, error message: {}".format(str(file.name), sys.exc_info()[0], str(e)))
        return None


# Verify the user arguments to the script are valid (input folder must found in the os, and of type directory)
def verify_user_input(args):
    script_syntax = "Try running again using script syntax: 'python list_files_to_csv.py <full_path_to_scan>'"
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


# Verify the result output file is exist and not empty
def verify_output_result_file(output_file):
    if not os.path.isfile(output_file) and os.path.getsize(output_file) > 0:
        print("Something in the output file is not OK.. exiting")
        exit(1)
    else:
        print("--- Success! Output file is created, please check it at path: {}\n".format(output_file))
        print("--- See the output of the csv below as well:")
        print(open(output_file, 'rb').read().decode(encoding='utf-8'))  # Print the result of output file into terminal


if __name__ == '__main__':
    verify_user_input(sys.argv)
    files_list = list_files(path=sys.argv[1])
    files_full_data = create_data_per_file(files_list)
    write_to_csv_file(files_full_data)
