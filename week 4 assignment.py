def file_processing_challenge():
    # Get input filename from user
    input_filename = input("Enter the name of the file to read: ")
    output_filename = input("Enter the name of the output file: ")
    
    try:
        # Read the input file
        with open(input_filename, 'r') as input_file:
            content = input_file.read()
        
        # Modify the content (example: convert to uppercase)
        modified_content = content.upper()
        
        # Write to the output file
        with open(output_filename, 'w') as output_file:
            output_file.write(modified_content)
        
        print(f"Success! Modified content written to {output_filename}")
    
    except FileNotFoundError:
        print(f"Error: The file '{input_filename}' does not exist.")
    except PermissionError:
        print(f"Error: Permission denied when accessing '{input_filename}'.")
    except IOError as e:
        print(f"An error occurred while processing the file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Run the program
file_processing_challenge()