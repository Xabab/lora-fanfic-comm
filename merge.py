import os

# Directory path
directory = 'txt/pool selected'

# List all text files in the directory
txt_files = [f for f in os.listdir(directory) if f.endswith('.txt')]

# Open the output file for writing
with open('RP_merged.txt', 'w') as outfile:
    # Loop through each text file and write its contents to the output file
    for file in txt_files:
        with open(os.path.join(directory, file), 'r') as infile:
            # Write the contents of the file to the output file
            outfile.write(infile.read())
            # Separate the text blocks with "\n\n\n"
            outfile.write('\n\n\n')
