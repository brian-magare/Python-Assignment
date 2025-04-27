import os

def main():
    print("=== File Processor with Error Handling ===")
    
    # Get input file name with validation
    input_file = get_valid_input_file()
    if not input_file:
        return
    
    # Read and process file content
    content = read_and_process_file(input_file)
    if content is None:
        return
    
    # Get output file name with validation
    output_file = get_valid_output_file()
    if not output_file:
        return
    
    # Write modified content
    write_output_file(output_file, content)
    print(f"\nSuccess! Modified content written to '{output_file}'")

def get_valid_input_file():
    """Get and validate input filename from user"""
    while True:
        try:
            filename = input("\nEnter input filename: ").strip()
            if not filename:
                print("Error: Filename cannot be empty.")
                continue
            
            # Check file exists and is readable
            if not os.path.exists(filename):
                raise FileNotFoundError(f"File '{filename}' does not exist")
            if not os.access(filename, os.R_OK):
                raise PermissionError(f"No read permission for '{filename}'")
            
            return filename
            
        except (FileNotFoundError, PermissionError) as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
        
        if not ask_retry("Try another input file?"):
            return None

def read_and_process_file(filename):
    """Read file content and return modified version"""
    try:
        with open(filename, 'r') as file:
            content = file.read()
        
        print("\nFile content preview:")
        print(content[:200] + ("..." if len(content) > 200 else ""))
        
        # Process content - example: add line numbers
        lines = content.splitlines()
        processed = [f"{i+1}: {line}" for i, line in enumerate(lines)]
        return "\n".join(processed)
        
    except UnicodeDecodeError:
        print("Error: Could not decode file content (try a different file)")
    except Exception as e:
        print(f"Error reading file: {e}")
    return None

def get_valid_output_file():
    """Get and validate output filename from user"""
    while True:
        try:
            filename = input("\nEnter output filename: ").strip()
            if not filename:
                print("Error: Filename cannot be empty.")
                continue
            
            # Check if file exists to prevent overwrite
            if os.path.exists(filename):
                if not ask_overwrite(filename):
                    continue
            
            # Check write permission
            dirname = os.path.dirname(filename) or "."
            if not os.access(dirname, os.W_OK):
                raise PermissionError(f"No write permission in '{dirname}'")
            
            return filename
            
        except PermissionError as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
        
        if not ask_retry("Try another output file?"):
            return None

def write_output_file(filename, content):
    """Write content to file with error handling"""
    try:
        with open(filename, 'w') as file:
            file.write(content)
    except Exception as e:
        print(f"Error writing file: {e}")
        raise

def ask_retry(prompt):
    """Ask user if they want to retry an operation"""
    while True:
        try:
            response = input(f"{prompt} (y/n): ").strip().lower()
            if response in ('y', 'yes'):
                return True
            if response in ('n', 'no'):
                return False
            print("Please enter 'y' or 'n'")
        except KeyboardInterrupt:
            return False

def ask_overwrite(filename):
    """Ask user if they want to overwrite existing file"""
    while True:
        try:
            response = input(f"File '{filename}' exists. Overwrite? (y/n): ").strip().lower()
            if response in ('y', 'yes'):
                return True
            if response in ('n', 'no'):
                return False
            print("Please enter 'y' or 'n'")
        except KeyboardInterrupt:
            return False

if __name__ == "__main__":
    main()