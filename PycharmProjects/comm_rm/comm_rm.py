import sys

def remove_comments(source_file, dest_file):
    in_multiline_comment = False
    with open(source_file, 'r') as src, open(dest_file, 'w') as dst:
        for line in src:
            stripped_line = line.strip()
            # Check for start of multi-line string/comment
            if stripped_line.startswith("'''") or stripped_line.startswith('"""'):
                # Toggle the in_multiline_comment flag if not in the middle of a multi-line comment
                if not in_multiline_comment or stripped_line.endswith("'''") or stripped_line.endswith('"""'):
                    in_multiline_comment = not in_multiline_comment
                    continue  # Skip adding this line
            # Check if we are not in a multi-line comment
            if not in_multiline_comment:
                # Handle single-line comments
                comment_start = line.find('#')
                if comment_start != -1:
                    line = line[:comment_start] + '\n'
            else:
                continue  # Skip lines that are part of a multi-line comment/string
            dst.write(line)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python comm_rm.py input_file.py")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = input_file.replace('.py', '_rm.py')
    remove_comments(input_file, output_file)
    print(f"Comments removed. Output saved to {output_file}")

