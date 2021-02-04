Usage example: python list_files_to_csv_multiprocessing.py /tmp/temp1/
Notes: did not handle case when no permissions to run the script, 
you will need to run chmod +x to script file if needed.

Generals: 
- Output of the csv file is also printed to terminal
- Used the multiprocssing code when calculating md5 using the files list as object to iterate over,
main methods: create_jobs_pool, create_file_data_using_multiprocessing, file_calc_worker.
- The csv file is saved to the same path as running the script (new file name: files_data.csv)  