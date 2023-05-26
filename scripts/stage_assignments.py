import argparse
import os
import shutil


def validate_paths(src, dest):

    # Check if src directory exists
    if not os.path.exists(src):
        err_msg = f"Source directory {src} does not exist."
        raise FileNotFoundError(f"Source directory '{src}' does not exist.")

    # Check if dest directory exists
    if os.path.exists(dest):
        err_msg = "Destination directory already exists."
        raise FileExistsError(err_msg)

    # Check if dest directory's dirname is valid
    dest_dirname = os.path.dirname(dest)
    if not os.path.isdir(dest_dirname):
        err_msg = f"Destnation directory's dirname {dest_dirname} is not valid."
        raise FleNotFoundError(err_msg)

    print("Path validation successful!")



def stage_student_repos(src, dest):

    # Create destination directory
    os.makedirs(dest)

    # Iterate through subdirectories in the source directory
    for subdir in os.scandir(src):
        if subdir.is_dir():
            # Get the name of the subdirectory
            subdir_name = subdir.name

            # Iterate through files in the subdirectory
            for file in os.scandir(subdir.path):
                if file.is_file() and file.name.endswith(".ipynb"):
                    # Get the filename without the extension
                    filename = os.path.splitext(file.name)[0]

                    # Create the new filename
                    new_filename = f"{subdir_name}_{filename}.ipynb"

                    # Copy the .ipynb file to the destination directory with the new filename
                    shutil.copy2(file.path, os.path.join(dest, new_filename))
                    shutil.chown(os.path.join(dest, new_filename), user=otter, group=otter)

    print("Student repositories staged successfully!")


if __name__ == "__main__":

    # To run:  python script_name.py /path/to/source /path/to/destination

    # Create argparse parser
    parser = argparse.ArgumentParser(description="Path validation script")
    parser.add_argument("src", type=str, help="Source directory path")
    parser.add_argument("dest", type=str, help="Destination directory path for staging files to be graded")

    # Parse command-line arguments
    args = parser.parse_args()

    # Validate paths
    validate_paths(args.src, args.dest)

    # Stage student repositories
    stage_student_repos(args.src, args.dest)
