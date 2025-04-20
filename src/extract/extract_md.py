import re
import os

def read_md_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def extract_md(md_content, pdf_name):
    janssen_file_path = "https://www.janssen.com/australia/sites/www_janssen_com_australia/files/prod_files/live/"
    document_path = janssen_file_path + pdf_name
    # Split content into lines for processing
    lines = md_content.splitlines()
    start_index = next((i for i, line in enumerate(lines) if re.match(r"^1\.\s+.*", line)), 0)
    lines = [lines[0]] + lines[start_index:]

    # The first line is the source
    source = lines[0].strip()

    results = []
    current_topic = None
    current_text = []
    table_mode = False
    table_data = {}
    current_table_section = None

    for line in lines:
        if table_mode and re.match(r"^\d+\.\s*", line):
            # If table data exists, save it as text for the current topic
            if current_topic and table_data:
                results.append({
                    "source": source,
                    "topic": current_topic,
                    "content": table_data,
                    "document": document_path
                })
                table_data = {}
            table_mode = False
        # Match lines that start with a number followed by a period and a question
        topic_match = re.match(r"^(\d+)\.\s*(.*?)\?$", line)
        if topic_match:
            # If there's a current topic, save it before starting a new one
            if current_topic and current_text:
                results.append({
                    "source": source,
                    "topic": current_topic,
                    "content": " ".join(current_text).strip(),
                    "document": document_path
                })
                current_text = []

            # Update the current topic
            current_topic = topic_match.group(2).strip()
        elif line.startswith("|") or line.startswith(" |"):
            # Process table rows
            table_mode = True
            if re.match(r"\|\s*\d+\s*\|", line) or line.startswith("|:"):
                continue
            cells = [cell.strip() for cell in line.strip('|').split('|')]
            if len(cells) == 2 and cells[0]:
                current_table_section = cells[0]
                if current_table_section not in table_data:
                    table_data[current_table_section] = []
                if cells[1]:
                    table_data[current_table_section].append(cells[1])
            elif current_table_section and cells[1]:
                table_data[current_table_section].append(cells[1])
        else:
            # Append non-empty lines to the current text block
            if line.strip():
                current_text.append(line.strip())

    # Save the last topic if present
    if current_topic and current_text:
        if table_mode and table_data:
            results.append({
                "source": source,
                "topic": current_topic,
                "content": table_data,
                "document": document_path
            })
        elif current_text:
            results.append({
                "source": source,
                "topic": current_topic,
                "content": " ".join(current_text).strip(),
                "document": document_path
            })

    return results

def process_md_file(pdf_path, file_path):
    # Read the markdown content from the file
    pdf_name = os.path.basename(pdf_path)
    md_content = read_md_file(file_path)

    # Parse the markdown content into structured data
    processed_result = extract_md(md_content, pdf_name)

    return processed_result
