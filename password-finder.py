import re
import os
import pathlib
from multiprocessing import Pool, cpu_count


#File type filtering
def is_target_file_type(file_path):
    if str(file_path).startswith('/var/mail'):
      return True
    target_extensions = {'.txt', '.config', '.conf', '.env'}
    return file_path.suffix.lower() in target_extensions

#Password/word filtering based of the below rules
def finder(string):
    min_length = 8
    max_length = 20
    
    if re.match(r'^[a-zA-Z_]\w*$', string) or '=' in string or ';' in string or re.search(r'\w+\.\w+', string):
        return False
    if string.startswith(('exports.', 'import ', 'from ', 'const ', 'var ', 'let ', '#' )):
        return False
    
    has_lowercase = re.search(r'[a-z]', string) is not None
    has_digits = re.search(r'[\d]', string) is not None
    has_symbols = re.search(r'[!@#$%^&*()]', string) is not None
    has_upper = re.search(r'[A-Z]', string) is not None
    
    return(
        len(string) >= min_length and
        len(string) <= max_length and
        has_digits and
        has_lowercase and
        has_upper and
        has_symbols
    )

#Applying the filters on each word
def password_checker(text):
    words = re.findall(r'\S+', re.sub(r'[,.;:()"\']', ' ', text))
    return [word for word in words if finder(word)]

#Skipping binaries
def is_text_file(file_path, block_size=512):
    try:
        with open(file_path, 'rb') as f:
            block = f.read(block_size)
            if not block:
                return True
            if b'\0' in block:
                return False
            return True
    except Exception:
        return False
                
#Scanning the directories
def scanRecurse(path, max_depth=20):
    if max_depth <= 0:
        return

    try:
        with os.scandir(path) as folders:
            for entry in folders:
                try:
                    if entry.is_symlink():
                        continue  # Skip symbolic links
                    if entry.is_dir():
                        if entry.name in {'proc', 'sys', 'run', 'dev'}:
                            continue  # Skip problematic system directories
                        if 'OneDrive' in entry.path:
                            continue 
                        yield from scanRecurse(entry.path, max_depth - 1)
                    elif entry.is_file() and is_target_file_type(pathlib.Path(entry.path)):
                        if entry.stat().st_size > 10 * 1024 * 1024:  # Skip files larger than 10 MB
                            print(f"Skipping large file: {entry.path}")
                            continue
                        yield entry.path
                except PermissionError:
                    print(f"Permission denied: {entry.path}")
                except OSError as e:
                    print(f"Error accessing {entry.path}: {e}")
    except PermissionError:
        print(f"Permission denied: {path}")
    except OSError as e:
        print(f"Error accessing {path}: {e}")   
#Reading the files
# def readFile(file_path):
#     if not is_text_file(file_path):
#         return ""
#     try:
#         file = pathlib.Path(file_path)
#         if file.is_file():
#             with open(file, 'r', encoding='utf-8', errors='ignore') as text:
#                 return text.read()
#     except TypeError:
#         pass
#     except PermissionError:
#         pass
#     except Exception as e:
#         print(f"Error reading file {file_path}: {str(e)}")
#     return ""


def process_file(file_path):
    try:
        file_path = os.path.normpath(file_path)
        with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
            content = file.read()
        potential_passwords = password_checker(content)
        if potential_passwords:
            return file_path, potential_passwords
    except Exception as e:
        print(f"Error processing file {file_path}: {str(e)}")
    return None

def main(dir_path):
    file_paths = list(scanRecurse(dir_path))
    for file_path in file_paths:
        result = process_file(file_path)
        if result:
            file_path, potential_passwords = result
            print(f"Potential passwords found in {file_path}:")
            print(potential_passwords)

if __name__ == "__main__":
    dir_path = input("Please provide the searching directory: ")
    main(dir_path)
