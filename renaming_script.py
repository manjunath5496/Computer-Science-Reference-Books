import os
import re
import shutil


def parse_markdown_table(md_file):
    # Read the markdown file
    with open(md_file, 'r') as f:
        md_content = f.read()

    # Define regex pattern to match links and their corresponding texts
    pattern = r'<a\s+target="_blank"\s+href="([^"]+)"\s+style="text-decoration:none;">([^<]+)</a>'

    # Find all matches in the markdown content
    matches = re.findall(pattern, md_content)

    # Create a dictionary mapping file names to their corresponding texts
    result_dict = {match[0].split('/')[-1]: match[1] for match in matches}

    return result_dict

def mkdown():
    # Provide the path to the markdown file
    markdown_file = 'README.md'

    # Parse the markdown file and extract information
    result = parse_markdown_table(markdown_file)

    # Print the resulting dictionary
    return result

def main():
    # Create a new directory for renamed PDFs
    os.makedirs('output', exist_ok=True)

    mapping = mkdown()
    
    # Iterate through each PDF in the 'books' directory
    for filename in os.listdir('books'):
        if filename.endswith('.pdf'):
            title = mapping.get(filename, "").strip().replace(" ", "_")
            if title == "":
                raise Exception("error no title")
            prefix = filename.replace(".pdf","").replace(r"comp(","").replace(")","")
            title = re.sub(r'\W+', '', title)
            new_filename = f"{prefix}_{title}.pdf"
            shutil.move(os.path.join('books', filename), os.path.join('output', new_filename))
            print(f"Renamed and copied {filename} to {new_filename}")
        else:
            print(f"Could not extract information from {filename}")

if __name__ == "__main__":
    main()
