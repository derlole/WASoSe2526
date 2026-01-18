import os

def create_file(filename, content):
    try:
        # Create (or overwrite) the file with specified content
        with open(filename, 'w') as file:
            file.write(content)
        print(f"File '{filename}' created successfully.")
    except IOError as e:
        print(f"An error occurred while creating the file: {e}")

def get_file_size(filename):
    try:
        # Get the size of the file in bytes
        return os.path.getsize(filename)
    except OSError as e:
        print(f"An error occurred while getting the file size: {e}")
        return None

def read_file_content(filename):
    try:
        # Read and return the content of the file
        with open(filename, 'r') as file:
            return file.read()
    except IOError as e:
        print(f"An error occurred while reading the file: {e}")
        return None

def main():
    filename = "example.txt"
    content = "This is a sample content for the file."

    # Create the file and write some content to it
    create_file(filename, content)

    # Get the size of the file
    file_size = get_file_size(filename)
    if file_size is not None:
        print(f"File size: {file_size} bytes")

    # Read and print the content of the file
    file_content = read_file_content(filename)
    if file_content is not None:
        print(f"File content:\n{file_content}")

if __name__ == "__main__":
    main()