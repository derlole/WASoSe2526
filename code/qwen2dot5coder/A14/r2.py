import os

def create_file(filename, content):
    try:
        with open(filename, 'w') as file:
            file.write(content)
        print(f"File '{filename}' created successfully.")
    except IOError as e:
        print(f"Error creating file '{filename}': {e}")

def get_file_size_and_content(filename):
    try:
        # Get the size of the file
        file_size = os.path.getsize(filename)
        
        # Read and display the content of the file
        with open(filename, 'r') as file:
            file_content = file.read()
        
        print(f"File '{filename}' size: {file_size} bytes")
        print("File content:")
        print(file_content)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except IOError as e:
        print(f"Error accessing file '{filename}': {e}")

def main():
    filename = 'example.txt'
    content = "Hello, this is a test file."
    
    # Create the file
    create_file(filename, content)
    
    # Get and display the size and content of the file
    get_file_size_and_content(filename)

if __name__ == "__main__":
    main()