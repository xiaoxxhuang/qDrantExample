import json

def process_text_by_topic(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    chunks = []
    current_topic = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Check if the line is a topic
        if not line.startswith(" ") and line.isalnum():
            current_topic = line
        else:
            # Treat the line as text under the current topic
            if current_topic:
                chunks.append({
                    "name": "React Use",
                    "topic": current_topic,
                    "text": line
                })

    # Write chunks to the output file
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(chunks, file, indent=4)

# Define input and output files
input_file = 'src/documentation/ReactUse.txt'
output_file = 'src/processed_chunks.json'

process_text_by_topic(input_file, output_file)
print(f"Processed chunks have been saved to {output_file}")