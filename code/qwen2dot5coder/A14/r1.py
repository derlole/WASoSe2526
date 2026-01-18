import os

def create_and_read_file(file_path, content):
    try:
        # Create and write to the file
        with open(file_path, 'w') as file:
            file.write(content)
        
        # Get the size of the file
        file_size = os.path.getsize(file_path)
        print(f"File created successfully. Size: {file_size} bytes")
        
        # Read the content of the file
        with open(file_path, 'r') as file:
            file_content = file.read()
            print("Content of the file:")
            print(file_content)
    
    except IOError as e:
        print(f"An error occurred while handling the file: {e}")

if __name__ == "__main__":
    file_path = "example.txt"
    content = "Hello, this is a test file created by the program."
    create_and_read_file(file_path, content)