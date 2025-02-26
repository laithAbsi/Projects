import sys

# Function to check if a string contains a valid date in the format DD/MM/YYYY
def contains_date(line):
    # Search for the pattern DD/MM/YYYY manually
    for i in range(len(line) - 9):  # The date must be 10 characters long
        if (line[i:i+2].isdigit() and line[i+2] == '/' and
            line[i+3:i+5].isdigit() and line[i+5] == '/' and
            line[i+6:i+10].isdigit()):
            return True
    return False

# Function to remove dated comments from the input file
def remove_dated_comments(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        in_multiline_comment = False
        multiline_buffer = []

        for line in infile:
            stripped_line = line.strip()

            # Check for single-line comments (//)
            if stripped_line.startswith("//"):
                # Check if it contains a date
                if not contains_date(stripped_line):
                    outfile.write(line)  # If no date, write the line as-is

            # Check for the start of a multi-line comment (/*)
            elif "/*" in stripped_line:
                in_multiline_comment = True
                multiline_buffer.append(line)  # Start collecting the multi-line comment

                # Check if it ends on the same line
                if "*/" in stripped_line:
                    in_multiline_comment = False
                    if not contains_date("".join(multiline_buffer)):
                        outfile.write("".join(multiline_buffer))  # Write the whole comment if no date
                    multiline_buffer = []

            # If inside a multi-line comment, keep collecting lines
            elif in_multiline_comment:
                multiline_buffer.append(line)
                if "*/" in stripped_line:  # End of multi-line comment
                    in_multiline_comment = False
                    if not contains_date("".join(multiline_buffer)):
                        outfile.write("".join(multiline_buffer))  # Write the whole comment if no date
                    multiline_buffer = []

            # Non-comment lines
            else:
                outfile.write(line)  # Write the line as-is

if __name__ == "__main__":
    # Check if enough arguments are passed
    if len(sys.argv) != 3:
        print("Usage: python dcom_rm.py inputC.cpp inputC_rm.cpp")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Call the function to remove dated comments
    remove_dated_comments(input_file, output_file)
