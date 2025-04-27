def file_processor():
    """Main function to handle file reading, processing, and writing with error handling"""
    while True:
        try:
            # Get input filename from user
            input_filename = input("Enter the name of the file to read: ").strip()
            
            # Read the file content with error handling
            try:
                with open(input_filename, 'r') as file:
                    content = file.read()
                print(f"\nSuccessfully read from '{input_filename}'")
                break
            except FileNotFoundError:
                print(f"\nError: The file '{input_filename}' does not exist.")
            except PermissionError:
                print(f"\nError: Permission denied when trying to read '{input_filename}'")
            except UnicodeDecodeError:
                print(f"\nError: Could not decode the contents of '{input_filename}' (try a different encoding)")
            except Exception as e:
                print(f"\nAn unexpected error occurred: {str(e)}")
            
            # Ask if user wants to try again
            if not try_again():
                return None

        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            return None

    # Process the content
    modified_content = process_content(content)

    # Get output filename from user
    while True:
        try:
            output_filename = input("\nEnter the name of the file to write to: ").strip()
            
            # Check if file exists to prevent overwrite
            try:
                with open(output_filename, 'x') as file:
                    file.write(modified_content)
                print(f"\nSuccessfully wrote modified content to '{output_filename}'")
                break
            except FileExistsError:
                print(f"\nError: The file '{output_filename}' already exists.")
                if not try_again("Would you like to try a different filename? (y/n): "):
                    return None
            except PermissionError:
                print(f"\nError: Permission denied when trying to write to '{output_filename}'")
            except Exception as e:
                print(f"\nAn unexpected error occurred: {str(e)}")
            
            if not try_again():
                return None

        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            return None

def process_content(content):
    """Process the file content and return modified version"""
    print("\nOriginal content preview:")
    print(content[:200] + ("..." if len(content) > 200 else ""))
    
    # Example modification: convert to uppercase and add line numbers
    modified_lines = []
    for i, line in enumerate(content.splitlines(), 1):
        modified_lines.append(f"Line {i}: {line.upper()}")
    
    return '\n'.join(modified_lines)

def try_again(prompt="Would you like to try again? (y/n): "):
    """Helper function to ask user if they want to retry"""
    while True:
        response = input(prompt).strip().lower()
        if response in ('y', 'yes'):
            return True
        elif response in ('n', 'no'):
            return False
        else:
            print("Please enter 'y' or 'n'.")

if __name__ == "__main__":
    print("=== File Processor with Error Handling ===")
    file_processor()