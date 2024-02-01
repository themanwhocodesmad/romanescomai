import os


def rename_files(path, prefix):
    # Ensure the path exists
    if not os.path.exists(path):
        print(f"The specified path '{path}' does not exist.")
        return

    # Counter to keep track of the number
    counter = 1

    # Iterate over all files in the directory
    for filename in os.listdir(path):
        # Split the original file name and extension
        name, extension = os.path.splitext(filename)

        # Create the new file name with the format: prefix-number.extension
        new_filename = f"{prefix}.{counter}{extension}"

        # Construct the full paths for the old and new file names
        old_filepath = os.path.join(path, filename)
        new_filepath = os.path.join(path, new_filename)

        try:
            # Rename the file
            os.rename(old_filepath, new_filepath)
            print(f"Renamed: {filename} to {new_filename}")
        except Exception as e:
            print(f"Error renaming {filename}: {e}")

        # Increment the counter for the next file
        counter += 1


# Get user input for path and prefix
path_to_rename = input("Enter the path of the folder: ")
prefix_to_add = input("Enter the prefix to add: ")

rename_files(path_to_rename, prefix_to_add)
