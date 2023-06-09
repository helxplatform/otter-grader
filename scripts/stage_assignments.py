import argparse
from datetime import datetime
import inspect
import os
import pathlib
import shutil
import time


def archive_previous_run(dest):
    print(f"Enter: {inspect.currentframe().f_code.co_name}")

    # Get archive dir path
    archive_dir = f"{dest}/archive"

    # Create archive dir if not present
    print(f"Creating archive directory {archive_dir}")
    create_dir(archive_dir)

    # Move any existing assignment dirs in staging dir to archive directory
    if os.path.exists(dest):
        subdirs = [f.path for f in os.scandir(dest) if f.is_dir() and \
                                                os.path.basename(f.name) != "archive" and \
                                                os.path.basename(f.name) != "repo_sync"]
        for subdir in subdirs:
            print(f"Moving {subdir} to {archive_dir}/{os.path.basename(subdir)}")
            os.system(f"mv {subdir} {archive_dir}/{os.path.basename(subdir)}")

    print(f"Exit: {inspect.currentframe().f_code.co_name}")


def create_dir(dir_name):
    print(f"Enter: {inspect.currentframe().f_code.co_name}, dir_name = [{dir_name}]")
    if not os.path.isdir(dir_name):
        try:
            print(f"Creating directory {dir_name}")
            os.makedirs(dir_name, mode = 0o750, exist_ok = True)
        except OSError as error:
            print(f"Directory {dir_name} can not be created")
            return False

    print(f"Exit: {inspect.currentframe().f_code.co_name}")

    return True


def stage_student_repos(assignment, src, dest):

    print(f"Enter: {inspect.currentframe().f_code.co_name}")

    archive_previous_run(dest)

    # Create destination directory
    date_time = datetime.fromtimestamp(time.time()) \
                        .strftime("%Y-%m-%d:%H:%M:%S")
    assignment_dir = f"{dest}/{assignment}-{date_time}"
    print(f"Creating assignment_dir {assignment_dir}")
    if not create_dir(assignment_dir):
        return False

    # Iterate through subdirectories in the source directory
    for srcdir in os.scandir(src):

        print(f"Processing subdir {srcdir.name}")

        # Exclude dest and archive subdirs if they're in the src directory
        if srcdir.is_dir() and \
           srcdir.name != os.path.basename(os.path.normpath(dest)) and \
           srcdir.name != 'repo_sync' and \
           srcdir.name != 'archive':
            print(f"Still processing subdir {srcdir.name}")

            # Iterate through files in the subdirectory
            # Copy student notebook(s) from each student_repo_name/assignment_name repo directory
            #    into dest/assignment_name-timestamp/student_repo_name-notebook_name.ipynb
            print(f"Scanning {os.path.join(srcdir.path, assignment)}")
            for file in os.scandir(os.path.join(srcdir.path, assignment)):
                if file.is_file() and file.name.endswith(".ipynb"):
                    print("Processing ipynb file {file.name}")
                    # Get the filename without the extension
                    filename = os.path.splitext(file.name)[0]

                    # Create the new filename
                    new_filename = f"{srcdir.name}_{filename}.ipynb"

                    print(f"New filename: {new_filename}")

                    # Copy the .ipynb file to the destination directory with the new filename
                    print(f"Copying {file.path} to {os.path.join(dest, assignment_dir, new_filename)}")
                    shutil.copy2(file.path, os.path.join(assignment_dir, new_filename))


    print("Student repositories staged successfully")
    print(f"Exit: {inspect.currentframe().f_code.co_name}")


if __name__ == "__main__":

    # To run: python script_name.py /path/to/source /path/to/destination
    #         python /scripts/stage_assignments.py assignment1 /data/course-1/repo_sync /data/course-1

    # Create argparse parser
    parser = argparse.ArgumentParser(description="Path validation script")
    parser.add_argument("assignment", type=str, help="Name of assignment to be staged")
    parser.add_argument("src", type=str, help="Source directory path")
    parser.add_argument("dest", type=str, help="Destination directory path for staging files to be graded")

    # Parse command-line arguments
    args = parser.parse_args()

    # Stage student repositories
    stage_student_repos(args.assignment, args.src, args.dest)
