import os
import sys

def main():
    print("📂 File Processor with Error Handling 📂")
    print("--------------------------------------")
    
    # Get input file with validation
    input_path = get_input_file()
    if not input_path:
        return
    
    # Read and process file
    content = read_and_process_file(input_path)
    if content is None:
        return
    
    # Get output file with validation
    output_path = get_output_file()
    if not output_path:
        return
    
    # Write processed content
    if write_output_file(output_path, content):
        print(f"\n✅ Success! Modified file saved to: {output_path}")
        print(f"📝 {len(content.splitlines())} lines processed")
    else:
        print("\n❌ Failed to write output file")

def get_input_file():
    """Get valid input file path from user"""
    while True:
        try:
            path = input("\n📥 Enter input file path: ").strip()
            
            if not path:
                print("⚠️ Error: Please enter a file path")
                continue
                
            path = os.path.abspath(path)
            
            # Check file exists
            if not os.path.exists(path):
                raise FileNotFoundError(f"File not found: {path}")
                
            # Check read access
            if not os.access(path, os.R_OK):
                raise PermissionError(f"No read permission: {path}")
                
            # Check if it's a file
            if not os.path.isfile(path):
                raise IsADirectoryError(f"Path is a directory: {path}")
                
            return path
            
        except (FileNotFoundError, PermissionError, IsADirectoryError) as e:
            print(f"❌ Error: {e}")
        except KeyboardInterrupt:
            print("\n🚫 Operation cancelled by user")
            return None
        except Exception as e:
            print(f"⚠️ Unexpected error: {e}")
            
        if not ask_retry("Try another input file?"):
            return None

def read_and_process_file(path):
    """Read file and return processed content"""
    try:
        print(f"\n🔍 Reading file: {path}")
        
        # Detect file size
        file_size = os.path.getsize(path)
        if file_size > 10 * 1024 * 1024:  # 10MB
            if not ask_confirmation(f"⚠️ Large file detected ({file_size/1024/1024:.1f} MB). Continue?"):
                return None
        
        # Read with encoding detection
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(path, 'r', encoding='latin-1') as f:
                content = f.read()
        
        print(f"📄 Read {len(content)} characters ({len(content.splitlines())} lines)")
        
        # Show preview
        preview_lines = content.splitlines()[:5]
        print("\nFile preview:")
        for i, line in enumerate(preview_lines, 1):
            print(f"{i}: {line[:80]}{'...' if len(line) > 80 else ''}")
        if len(content.splitlines()) > 5:
            print("... (truncated)")
        
        # Process content - example: add line numbers
        processed_lines = []
        for i, line in enumerate(content.splitlines(), 1):
            processed_lines.append(f"{i:4d} | {line}")
        
        return '\n'.join(processed_lines)
        
    except Exception as e:
        print(f"❌ Error processing file: {e}")
        return None

def get_output_file():
    """Get valid output file path from user"""
    while True:
        try:
            path = input("\n📤 Enter output file path: ").strip()
            
            if not path:
                print("⚠️ Error: Please enter a file path")
                continue
                
            path = os.path.abspath(path)
            dirname = os.path.dirname(path)
            
            # Check directory exists
            if dirname and not os.path.exists(dirname):
                if ask_confirmation(f"Directory doesn't exist. Create it? ({dirname})"):
                    os.makedirs(dirname)
                else:
                    continue
                    
            # Check write access
            if os.path.exists(path):
                if not ask_confirmation(f"File exists. Overwrite? ({path})"):
                    continue
            else:
                if dirname and not os.access(dirname, os.W_OK):
                    raise PermissionError(f"No write permission in: {dirname}")
                    
            return path
            
        except PermissionError as e:
            print(f"❌ Error: {e}")
        except KeyboardInterrupt:
            print("\n🚫 Operation cancelled by user")
            return None
        except Exception as e:
            print(f"⚠️ Unexpected error: {e}")
            
        if not ask_retry("Try another output file?"):
            return None

def write_output_file(path, content):
    """Write content to file with error handling"""
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"❌ Error writing file: {e}")
        return False

def ask_retry(prompt):
    """Ask user to retry an operation"""
    while True:
        try:
            response = input(f"\n{prompt} (y/n): ").strip().lower()
            if response in ('y', 'yes'):
                return True
            if response in ('n', 'no'):
                return False
            print("⚠️ Please enter 'y' or 'n'")
        except KeyboardInterrupt:
            return False

def ask_confirmation(prompt):
    """Ask user for confirmation"""
    while True:
        try:
            response = input(f"{prompt} (y/n): ").strip().lower()
            if response in ('y', 'yes'):
                return True
            if response in ('n', 'no'):
                return False
            print("⚠️ Please enter 'y' or 'n'")
        except KeyboardInterrupt:
            return False

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"💥 Critical error: {e}")
        sys.exit(1)