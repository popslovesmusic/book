import os

def list_all_directories(start_path):
    output = []
    for root, dirs, files in os.walk(start_path):
        # Calculate level for indentation, ensuring it's 0 for the start_path itself
        relative_path = os.path.relpath(root, start_path)
        level = relative_path.count(os.sep) if relative_path != '.' else 0

        indent = ' ' * 4 * (level)
        
        # Append directory name
        output.append(f'{indent}[DIR] {os.path.basename(root)}/')
        
        # Append files in current directory
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            output.append(f'{subindent}{f}')
    return "\n".join(output)

current_working_directory = os.getcwd()
output_content = list_all_directories(current_working_directory)

with open(os.path.join(current_working_directory, "directory_index.txt"), "w", encoding="utf-8") as f:
    f.write(output_content)