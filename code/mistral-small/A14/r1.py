import os

def create_and_display_file(filename, content):
    try:
        # Write content to the file
        with open(filename, 'w') as file:
            file.write(content)
        print(f"File '{filename}' created successfully.")

        # Get file size
        file_size = os.path.getsize(filename)
        print(f"Size of the file '{filename}': {file_size} bytes")

        # Read and display file content
        with open(filename, 'r') as file:
            file_content = file.read()
        print(f"Content of the file '{filename}':\n{file_content}")

    except FileNotFoundError:
        print("An error occurred while accessing the file system.")
    except PermissionError:
        print("Permission denied while trying to access the file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Define filename and content
filename = 'example.txt'
content = "This is a sample text to demonstrate file creation and reading."

# Call the function
create_and_display_file(filename, content)