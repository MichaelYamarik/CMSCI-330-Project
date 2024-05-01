import os

def combine_sec_files():
    # Get the current working directory
    current_directory = os.getcwd()

    # Get a list of all files in the directory
    files = os.listdir(current_directory)

    # Filter out only the files ending with ".sec"
    sec_files = [file for file in files if file.endswith(".sec")]

    # If there are no .sec files, print a message and return
    if not sec_files:
        print("No .sec files found in the directory.")
        return

    # Create a dictionary to store lines with their respective file names
    combined_lines = {}

    # Iterate over each .sec file
    for sec_file in sec_files:
        with open(sec_file, "r") as f:
            # Read the contents of the .sec file line by line
            for line in f:
                # Strip newline characters and leading/trailing whitespaces
                line = line.strip()
                # Append the current file name after each line
                line_with_file_name = f"{line} - {sec_file}"
                # Add the line to the dictionary
                combined_lines[line_with_file_name] = None

    # Sort the combined lines alphabetically
    sorted_lines = sorted(combined_lines.keys())

    # Write the sorted lines to the combined text file
    with open("combined_text.txt", "w") as combined_file:
        for line in sorted_lines:
            combined_file.write(line + "\n")

    print("Combined and sorted text file created: combined_text.txt")

# Call the function to combine and sort .sec files
combine_sec_files()
